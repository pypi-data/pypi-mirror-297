from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print
import os
import time
import requests
from datetime import datetime
import sys

console = Console()

# Dictionary mapping our license names to GitHub API identifiers
license_identifiers = {
    "MIT License": "mit",
    "Apache License 2.0": "apache-2.0",
    "GNU General Public License v3.0 (GPL-3.0)": "gpl-3.0",
    "GNU Lesser General Public License v3.0 (LGPL-3.0)": "lgpl-3.0",
    "GNU Affero General Public License v3.0 (AGPL-3.0)": "agpl-3.0",
    "Mozilla Public License 2.0 (MPL-2.0)": "mpl-2.0",
    "BSD 2-Clause 'Simplified' License": "bsd-2-clause",
    "BSD 3-Clause 'New' or 'Revised' License": "bsd-3-clause",
    "Eclipse Public License 2.0": "epl-2.0",
    "Creative Commons Attribution 4.0 International (CC BY 4.0)": "cc-by-4.0",
    "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)": "cc-by-nc-4.0",
    "The Unlicense": "unlicense"
}

# License summaries for quick reference
license_summaries = {
    "MIT License": "A short and permissive license that allows reuse with few restrictions.",
    "Apache License 2.0": "A permissive license similar to MIT but includes an explicit grant of patent rights.",
    "GNU General Public License v3.0 (GPL-3.0)": "A strong copyleft license requiring derived works to be licensed under GPL.",
    "GNU Lesser General Public License v3.0 (LGPL-3.0)": "A weak copyleft license that allows linking to proprietary modules.",
    "GNU Affero General Public License v3.0 (AGPL-3.0)": "A strong copyleft license designed for network server software.",
    "Mozilla Public License 2.0 (MPL-2.0)": "A weak copyleft license that allows combining with proprietary code under certain conditions.",
    "BSD 2-Clause 'Simplified' License": "A permissive license with minimal restrictions on reuse.",
    "BSD 3-Clause 'New' or 'Revised' License": "Similar to BSD 2-Clause but includes a non-endorsement clause.",
    "Eclipse Public License 2.0": "A weak copyleft license used by the Eclipse Foundation.",
    "Creative Commons Attribution 4.0 International (CC BY 4.0)": "Allows sharing and adaptation with attribution.",
    "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)": "Allows sharing and adaptation with attribution for non-commercial purposes.",
    "The Unlicense": "A license that dedicates the work to the public domain."
}

def ask_question(question, choices, help_text):
    console.print("\n\n")  # Add two blank lines for spacing
    while True:
        response = Prompt.ask(question, choices=choices + ['?'])
        if response.lower() == '?':
            console.print(f"\n[italic cyan]{help_text}[/italic cyan]\n")
        else:
            return response.lower()

def get_license_text(license_name):
    identifier = license_identifiers.get(license_name)
    if not identifier:
        return f"Unable to fetch license text for {license_name}. Please refer to the official license website."
    
    url = f"https://api.github.com/licenses/{identifier}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['body']
        else:
            return f"Unable to fetch license text for {license_name}. Please refer to the official license website."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the license: {e}"

def main():
    console.print(Panel.fit("Welcome to the Open Source License Selector", border_style="bold green"))
    
    console.print("\n[bold green]This tool will help you select an appropriate open-source license for your project.[/bold green]")
    
    time.sleep(1)
    
    console.print("\n\n[bold red]LEGAL DISCLAIMER:[/bold red] This tool provides general information about open-source licenses but does not offer legal advice. For legal advice, please consult a qualified attorney. The use of this tool does not create an attorney-client relationship.")
    
    time.sleep(2)
    console.print("\n\n[bold green]Please answer the following questions to help us recommend a license for your project.[/bold green]")
    time.sleep(1)
    console.print("[italic]\nType '?' at any prompt to get more information about the question.[/italic]")
    time.sleep(1)
    
    # Step 1: Project Type
    project_type_help = (
        "software: For code-based projects\n"
        "content: For non-code projects like documentation or media\n"
        "both: For projects that include both software and content"
    )
    project_type = ask_question(
        "What type of project are you working on?",
        choices=["software", "content", "both"],
        help_text=project_type_help
    )
    
    # ... (keep the rest of the main function code)

    # Display Recommended License(s)
    if project_type == "both":
        console.print(f"\n\n[bold green]Recommended Licenses:[/bold green]")
        console.print(f"Software License: {license}")
        console.print(f"Content License: {content_license}")
    else:
        console.print(f"\n\n[bold green]Recommended License:[/bold green] {license}")
        content_license = license  # Set content_license to the same as license for non-"both" cases

    # Display License Summary
    console.print(f"\n[bold blue]Summary:[/bold blue] {license_summaries.get(license, 'No summary available.')}")
    
    if project_type == "both":
        console.print(f"\n[bold blue]Content License Summary:[/bold blue] {license_summaries.get(content_license, 'No summary available.')}")
    
    # Offer to Write License File(s)
    console.print("\n")  # Add blank line for spacing
    write_file = Confirm.ask("Do you want to create a LICENSE file with the recommended license in the current directory?")
    
    if write_file:
        # Get Author Name and Current Year
        author_name = Prompt.ask("Please enter your name to include in the license")
        current_year = datetime.now().year
        
        # Fetch and Write Software License Text
        license_text = get_license_text(license)
        license_text = license_text.replace("[year]", str(current_year))
        license_text = license_text.replace("[fullname]", author_name)
        
        with open("LICENSE", "w") as f:
            f.write(license_text)
        console.print("\n[bold green]LICENSE file created successfully with full license text![/bold green]")
        
        # If Both, Also Write Content License
        if project_type == "both":
            content_license_text = get_license_text(content_license)
            content_license_text = content_license_text.replace("[year]", str(current_year))
            content_license_text = content_license_text.replace("[fullname]", author_name)
            
            with open("CONTENT_LICENSE", "w") as f:
                f.write(content_license_text)
            console.print("[bold green]CONTENT_LICENSE file created successfully with full license text![/bold green]")
    else:
        console.print("\n[bold yellow]Remember to include the license text in your project to comply with the license terms.[/bold yellow]")

if __name__ == "__main__":
    sys.exit(main())