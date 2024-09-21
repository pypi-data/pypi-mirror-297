from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print
import os
import time
import requests
from datetime import datetime

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
        "Software: For code-based projects\n"
        "Content: For non-code projects like documentation or media\n"
        "Both: For projects that include both software and content"
    )
    project_type = ask_question(
        "What type of project are you working on?",
        choices=["Software", "Content", "Both"],
        help_text=project_type_help
    )
    
    if project_type == "software":
        # Step 2: Permissive vs Copyleft
        permissive_help = (
            "Permissive License: Allows others to use, modify, and distribute your code with minimal restrictions.\n"
            "Copyleft License: Requires that anyone who distributes your code or a derivative work must make the source available under the same terms."
        )
        permissive = ask_question(
            "Do you want to allow others to use your code freely without requiring them to share their modifications?",
            choices=['y', 'n'],
            help_text=permissive_help
        )
        
        if permissive == 'y':
            # Step 3: Patent Concerns
            patent_help = "Patent Grant: Provides users with an explicit license to any patents covering the software."
            patent_concerns = ask_question(
                "Are you concerned about patents and want to provide an explicit patent license?",
                choices=['y', 'n'],
                help_text=patent_help
            )
            if patent_concerns == 'y':
                license = "Apache License 2.0"
            else:
                license = "MIT License"
        else:
            # Step 3: Copyleft Strength
            copyleft_help = (
                "Strong Copyleft: Requires that derivative works and all software linked with it be released under the same license.\n"
                "Weak Copyleft: Requires that modifications to your code be shared under the same license, but allows linking with proprietary code."
            )
            copyleft_strength = ask_question(
                "Do you want a strong or weak copyleft?",
                choices=["Strong", "Weak"],
                help_text=copyleft_help
            )
            if copyleft_strength == "strong":
                # Step 4: Network Use
                network_help = "Network Use: Applies to software used over a network (e.g., web applications)."
                network_use = ask_question(
                    "Is your software likely to be used over a network, and do you want the copyleft to apply in this case?",
                    choices=['y', 'n'],
                    help_text=network_help
                )
                if network_use == 'y':
                    license = "GNU Affero General Public License v3.0 (AGPL-3.0)"
                else:
                    license = "GNU General Public License v3.0 (GPL-3.0)"
            else:
                # Weak Copyleft License
                license = "Mozilla Public License 2.0 (MPL-2.0)"
    
    elif project_type == "content":
        # Content Licenses
        content_help = "Creative Commons Licenses: Designed for content like documentation, media, etc."
        commercial_use = ask_question(
            "Do you want to allow commercial use of your content?",
            choices=['y', 'n'],
            help_text=content_help
        )
        if commercial_use == 'y':
            license = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
        else:
            license = "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"
    
    elif project_type == "both":
        # Mixed Project Type
        console.print("\n\n[bold]Since your project includes both software and content, you might need to apply different licenses to different parts of your project.[/bold]")
        console.print("We recommend choosing appropriate licenses for each component.")
        
        # Software Component
        software_help = (
            "Permissive License: Allows others to use, modify, and distribute your code with minimal restrictions.\n"
            "Copyleft License: Requires that anyone who distributes your code or a derivative work must make the source available under the same terms."
        )
        permissive = ask_question(
            "Do you want to allow others to use your code freely without requiring them to share their modifications?",
            choices=['y', 'n'],
            help_text=software_help
        )
        
        if permissive == 'y':
            # Patent Concerns
            patent_help = "Patent Grant: Provides users with an explicit license to any patents covering the software."
            patent_concerns = ask_question(
                "Are you concerned about patents and want to provide an explicit patent license?",
                choices=['y', 'n'],
                help_text=patent_help
            )
            if patent_concerns == 'y':
                license = "Apache License 2.0"
            else:
                license = "MIT License"
        else:
            # Copyleft Strength
            copyleft_help = (
                "Strong Copyleft: Requires that derivative works and all software linked with it be released under the same license.\n"
                "Weak Copyleft: Requires that modifications to your code be shared under the same license, but allows linking with proprietary code."
            )
            copyleft_strength = ask_question(
                "Do you want a strong or weak copyleft?",
                choices=["Strong", "Weak"],
                help_text=copyleft_help
            )
            if copyleft_strength == "strong":
                # Network Use
                network_help = "Network Use: Applies to software used over a network (e.g., web applications)."
                network_use = ask_question(
                    "Is your software likely to be used over a network, and do you want the copyleft to apply in this case?",
                    choices=['y', 'n'],
                    help_text=network_help
                )
                if network_use == 'y':
                    license = "GNU Affero General Public License v3.0 (AGPL-3.0)"
                else:
                    license = "GNU General Public License v3.0 (GPL-3.0)"
            else:
                # Weak Copyleft License
                license = "Mozilla Public License 2.0 (MPL-2.0)"
        
        # Content Component
        content_help = "Creative Commons Licenses: Designed for content like documentation, media, etc."
        commercial_use = ask_question(
            "Do you want to allow commercial use of your content?",
            choices=['y', 'n'],
            help_text=content_help
        )
        if commercial_use == 'y':
            content_license = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
        else:
            content_license = "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"
    else:
        console.print("\n[bold red]Invalid project type selected. Please restart the tool and choose a valid option.[/bold red]")
        return
    
    # Display Recommended License(s)
    if project_type == "both":
        console.print(f"\n\n[bold green]Recommended Licenses:[/bold green]")
        console.print(f"Software License: {license}")
        console.print(f"Content License: {content_license}")
    else:
        console.print(f"\n\n[bold green]Recommended License:[/bold green] {license}")
    
    # Display License Summary
    console.print(f"\n[bold blue]Summary:[/bold blue] {license_summaries.get(license, 'No summary available.')}")
    
    if project_type == "both":
        console.print(f"\n[bold blue]Content License Summary:[/bold blue] {license_summaries.get(content_license, 'No summary available.')}")
    
    # Offer to Write License File(s)
    console.print("\n")  # Add blank line for spacing
    write_file = Confirm.ask("Do you want to create a LICENSE file with the recommended license?")
    
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
    main()
