from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(doc_id: str = Field(description="ID of document to read")):
    if doc_id not in docs:
        return ValueError(f"Doc with ID {doc_id} not found")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document.",
)
def edit_document(
    doc_id: str = Field(description="ID of document to read"),
    old_str: str = Field(description="Text to replace. Must match exactly."),
    new_str: str = Field(description="New text to insert in place of the old text"),
):
    if doc_id not in docs:
        return ValueError(f"Doc with ID {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    """Resource to return all doc IDs"""
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plan")
def fetch_doc(doc_id: str) -> str:
    """Resource to return the contents of a particular doc"""
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format", description="Rewrite the contents of a document in Markdown format"
)
def format_doc(
    doc_id: str = Field(description="ID of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with Markdown syntax.

    The ID od the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary.
    Use the 'edit_document' tool to edit the document.
    """
    return [base.UserMessage(prompt)]


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
