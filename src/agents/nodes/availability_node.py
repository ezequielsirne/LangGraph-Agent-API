from datetime import datetime
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from src.agents.schemas import AvailabilityInput
from src.agents.tools import check_availability
from src.agents.state import GraphState

# Set up the LLM and the output parser
llm = ChatOpenAI(model="gpt-4", temperature=0)
parser = PydanticOutputParser(pydantic_object=AvailabilityInput)

# Prompt template for extracting reservation dates from user messages
availability_prompt = PromptTemplate.from_template(
    """
You are a helpful assistant for hotel reservations.

Today's date is: {current_date}

From the following message, extract the check-in and check-out dates for an apartment reservation.
The user might refer to weekends, specific days, or use ambiguous expressions. 
Convert these dates to ISO 8601 format (YYYY-MM-DDTHH:MM:SS).

Message: "{message}"

{format_instructions}
"""
)

# Node for availability lookup
def availability_node(state: GraphState) -> GraphState:
    user_input = state["user_input"]
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Format the prompt with user input and current date
    prompt = availability_prompt.format_prompt(
        current_date=current_date,
        message=user_input,
        format_instructions=parser.get_format_instructions()
    )

    # Invoke the language model and parse the output
    response = llm.invoke(prompt.to_string())
    availability_input = parser.parse(response.content)

    # Call the availability tool
    result = check_availability.invoke({
        "checkin": availability_input.checkin,
        "checkout": availability_input.checkout
    })

    # Update the conversation state with availability information and parsed dates
    return {
        **state,
        "availability": result,
        "parsed_availability_input": {
            "checkin": availability_input.checkin,
            "checkout": availability_input.checkout
        }
    }

# Runnable version of the node for use in the LangGraph
availability_node_runnable = RunnableLambda(availability_node)

# Simple test runner for development purposes
if __name__ == "__main__":
    import json

    test_inputs = [
        "¿Hay disponibilidad para el próximo fin de semana?",
        "Quisiera reservar del 5 al 7 de mayo",
        "Del viernes al domingo que viene hay algo?",
        "Busco hospedaje el último finde del mes",
        "¿Tienen algo disponible para el primer fin de semana de junio?",
    ]

    for idx, input_text in enumerate(test_inputs, 1):
        print(f"\nTest #{idx}")
        try:
            # Simulated state
            fake_state = {
                "conversation_history": [],
                "user_input": input_text,
                "info_docs": None,
                "availability": None
            }

            # Run the node
            updated_state = availability_node(fake_state)

            # Print the output
            print("User input:", input_text)
            print("Parsed dates:", updated_state["parsed_availability_input"])
            print("Availability output:")
            print(json.dumps(updated_state["availability"], indent=2))

        except Exception as e:
            print(f"Error in test #{idx}: {e}")
