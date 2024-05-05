import os
import re
from subprocess import call
def gather_markdown_files(summary_file):
  """
  Extracts markdown file references from a summary file.

  Args:
      summary_file: Path to the summary file (e.g., "summery.md").

  Returns:
      A list of markdown file paths.
  """
  markdown_files = []
  with open(summary_file, 'r') as f:
    for line in f:
      # Regex to match filename within brackets ending with .md
      match = re.search(r"\[[^\]]+\]\(([^)]+)\.md\)", line)
      if match:
        markdown_files.append(match.group(1) + ".md")  # Extract captured group (file path)
  return markdown_files

def generate_pdf(markdown_files, output_file):
  """
  Combines markdown files into a single PDF using pandoc.

  Args:
      markdown_files: List of markdown file paths.
      output_file: Path to the output PDF file.
  """
  command = ["pandoc", "--pdf-engine=xelatex"]
  for file in markdown_files:
    command.append(file)
  command.append("-o")
  command.append(output_file)
  print("Command: " + " ".join(command))

  call(command)

if __name__ == "__main__":
  summary_file = "SUMMARY.md"  # Replace with your summary file name
  output_file = "combined_documentation.docx"  # Replace with desired output name
  markdown_files = gather_markdown_files(summary_file)
  generate_pdf(markdown_files, output_file)
  print(f"Combined markdown files into {output_file}")