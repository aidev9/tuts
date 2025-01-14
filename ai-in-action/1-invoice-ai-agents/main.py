import os
from typing import List, TypedDict
from colorama import Fore
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Create an invoice markdown file
def create_invoice_markdown(file_path: str):
    invoice_text = """
    # Invoice

    **Client:** ABC Corp  
    **Address:** 123 Business Rd, Suite 100, Business City, BC 12345  
    **Invoice Date:** 2025-01-23  
    **Due Date:** 2025-02-23
    **Payment Terms:** Net30  

    ## Services
    1. Web Development - $150,000
    2. SEO Optimization - $50,000
    3. Social Media Management - $30,000
    4. Content Creation - $26,000
    5. Email Marketing - $20,000
    6. Graphic Design - $10,000

    **Notes:**  
    Please make the payment by the due date to avoid any late fees. If you have any questions regarding this invoice, feel free to contact us at billing@abccorp.com.

    **Bank Details:**  
    Bank Name: Business Bank  
    Account Number: 123456789  
    Routing Number: 987654321  
    SWIFT Code: BUSB1234  

    **Contact Information:**  
    Phone: (123) 456-7890  
    Email: support@abccorp.com  
    """
    with open(file_path, "w") as file:
        file.write(invoice_text)

# Read the invoice markdown file
def read_invoice_markdown(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

# Define the State schema
class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    cost_of_services: float
    total_amount_due: float
    profitability: str
    summary: str

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Classify the client tier based on the invoice amount
def node_classify_client(state: State):
    ''' Classify the client tier based on the invoice amount '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Classify the client tier based on the invoice amount into one of the categories: Silver, Gold, Platinum.
        - Silver: $0-100,000
        - Gold: $100,000-1,000,000
        - Platinum: Over $1,000,000
        
        Invoice Info: {text}
        
        Category:
        """
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    classification = llm.invoke([message]).content.strip()
    state["classification"] = classification
    return state

# Extract total amount due
def node_extract_invoice_amount(state: State):
    ''' Extract total amount due '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract the Total Amount Due.\n\nText:{text}. Return the number only."
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    result = llm.invoke([message]).content.strip().split(", ")
    state["total_amount_due"] = result[0]
    return state

# Extract key entities such as client, services, payment terms
def node_extract_entities(state: State):
    ''' Extract key entities such as client, services, payment terms '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract the following entities from the text: Client, Services, Payment Terms.\n\nText:{text}\n\nEntities:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    entities = llm.invoke([message]).content.strip().split(", ")
    state["entities"] = entities
    return state

# Analyze the profitability based on the cost of services and total amount due
def node_analyze_profitability(state: State):
    ''' Analyze the profitability based on the cost of services and total amount due '''
    total_amount_due = state["total_amount_due"]
    total_amount_due = float(total_amount_due)
    cost_of_services = state["cost_of_services"]
    profit = total_amount_due - cost_of_services
    profitability = "Profitable" if profit > 0 else "Not Profitable"
    state["profitability"] = profitability
    return state

# Summarize the text in several short sentences
def node_summarize(state: State):
    ''' Summarize the text in several short sentences '''
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in several short sentences.\n\nText:{text}\n\nSummary:"
    )
    message = HumanMessage(content=prompt.format(text=state["text"]))
    summary = llm.invoke([message]).content.strip()
    state["summary"] = summary
    return state

# Create a graph
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("classify_client", node_classify_client)
workflow.add_node("extract_entities", node_extract_entities)
workflow.add_node("extract_invoice_amount", node_extract_invoice_amount)
workflow.add_node("analyze_profitability", node_analyze_profitability)
workflow.add_node("summarize", node_summarize)

# Add edges to the graph
workflow.set_entry_point("classify_client") # Set the entry point of the graph
workflow.add_edge("classify_client", "extract_entities")
workflow.add_edge("extract_entities", "extract_invoice_amount")
workflow.add_edge("extract_invoice_amount", "analyze_profitability")
workflow.add_edge("analyze_profitability", "summarize")
workflow.add_edge("summarize", END)

# Compile the graph
graph = workflow.compile()

# Draw the graph
try:
    graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")
except Exception:
    pass

# Process the invoice
def process_invoice(invoice_text: str, cost_of_services: float):
    state = State(text=invoice_text, classification="", entities=[], summary="", cost_of_services=cost_of_services)
    result = graph.invoke(state)
    return result

# Run the graph
if __name__ == "__main__":
    invoice_file_path = "./data/invoice.md"
    create_invoice_markdown(invoice_file_path)
    invoice_text = read_invoice_markdown(invoice_file_path)
    cost_of_services = 264000  # Example cost of services
    result = process_invoice(invoice_text, cost_of_services)
    print(Fore.CYAN, "Invoice Text:", invoice_text, "\n")
    print(Fore.YELLOW, "Client Classification:", result["classification"], "\n")
    print(Fore.GREEN, "Total amount due:", result["total_amount_due"], "\n")
    print(Fore.MAGENTA, "Cost of services:", cost_of_services, "\n")
    print(Fore.BLUE, "Profitability:", result["profitability"], "\n")
    print(Fore.WHITE, "Entities:", result["entities"], "\n")
    print(Fore.RED, "Summary:", result["summary"], "\n")