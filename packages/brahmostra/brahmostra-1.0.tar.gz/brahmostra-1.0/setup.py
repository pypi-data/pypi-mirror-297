from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0'
DESCRIPTION = '## *Brahmostra: The Ultimate Code Generation and File Management Tool*'
LONG_DESCRIPTION = '''
## *Brahmostra: The Ultimate Code Generation and File Management Tool*

*Brahmostra* is a powerful, multipurpose tool designed to streamline the workflow of developers, enabling them to effortlessly generate, manage, and handle code files in various programming languages. By integrating with advanced AI models, Brahmostra simplifies the process of coding, while offering a comprehensive suite of file management capabilities.

### *Key Features*:

1. *AI-Powered Code Generation*: 
   Brahmostra allows you to generate fully-functional code in multiple languages using state-of-the-art models. With support for various programming languages like Python, JavaScript, Bash, and more, this tool is ideal for automating routine coding tasks or generating solutions from scratch based on user prompts. The code is automatically checked for syntax errors to ensure reliability before execution.

2. *Comprehensive File Management*: 
   Brahmostra isn't just about code generation—it's also a powerful file management tool. Users can:
   - *List, Delete, and Rename* files with ease.
   - *Duplicate* any generated file for backup or experimentation.
   - *Batch Delete* files to clean up large sets of old or unused code.
   - *Schedule File Deletion*, allowing users to set time delays for when files should be deleted.
   - *Archive* multiple files into a .zip archive for backup or distribution.
   - *Search for Keywords* in files to quickly locate important content.

3. *Logging and Exporting*:
   Every action taken within Brahmostra, from code generation to file deletion, is logged for accountability. These logs can easily be *exported* for auditing purposes or to keep track of development history.

4. *Undo Functionality*:
   Made a mistake? Brahmostra’s undo functionality allows you to *restore deleted files*, minimizing accidental data loss.

5. *Clipboard Integration*:
   With a single command, Brahmostra allows users to *copy the content of a file to the clipboard* for quick sharing or pasting into other applications.

6. *Remote Backup Support*:
   Brahmostra also supports *backing up files to a remote server* using SCP (via paramiko), providing a robust solution for protecting your work in case of local machine failures.

7. *Code Summarization*:
   If you have a large code file and need a brief overview, Brahmostra offers an integrated *code summarization* feature. This feature breaks down complex code into concise, understandable summaries to help developers quickly understand the logic of generated or existing scripts.

### *How It Works*:

Brahmostra’s user interface is driven through a command-line interface (CLI). The tool integrates with advanced AI models to generate code based on user prompts. Additionally, it features a simple and intuitive menu system that allows users to access file management and log functions seamlessly.

### *Use Cases*:

- *Rapid Prototyping*: Developers can quickly generate working prototypes in different languages without having to write all the boilerplate code manually.
- *Automated Scripting*: With Brahmostra, common tasks like file handling or data processing scripts can be generated effortlessly.
- *Project Management*: Brahmostra's file archiving, backup, and scheduled deletion features make it easy to manage large coding projects over time.
- *Team Collaboration*: By copying code to the clipboard or exporting logs, team members can easily share their progress and work together efficiently.

---

*Brahmostra* stands out as a comprehensive, all-in-one solution for coders and software engineers. Whether you need to generate quick scripts, manage a repository of files, or protect your work with remote backups, Brahmostra has all the tools you need, delivered in one easy-to-use package.

Let *Brahmostra* be your ultimate weapon in the world of development and code management!
'''

# Setting up
setup(
    name="brahmostra",
    version=VERSION,
    author="Suraj sharma",
    author_email="Surajsharma963472@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'groq',
    ],
    keywords=['Surya', 'brahmostra', 'code', 'python tutorial', 'Suraj'],
)