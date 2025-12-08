![GitHub repo size](https://img.shields.io/github/repo-size/VivIngInf/VivereFiligrana)
![GitHub License](https://img.shields.io/github/license/VivIngInf/VivereFiligrana)

# Vivere Filigrana - Document Conversion and Watermarking Tool

## Language Toggle

[🇮🇹 Italiano](./resources/docs/README-italian.md) | [🇬🇧 English](#)

## Introduction

Welcome to the Vivere Ateneo document conversion and watermarking tool: Vivere Filigrana!

This website allows users to convert `.docx` files into `.pdf` and apply a watermark with the Vivere Ateneo logo and its sub-associations.

Additionally, users can directly upload `.pdf` files, and the tool will apply the watermark to them.

## Project Structure

Here is the directory structure of the project:

```MD
┌── resources 🌍
│   ├── images 🖼️               # Contains image assets used in the readmes
│   └── docs 📚                 # Stores any README or documentation files
├── source ⚙️
│   ├── static 🌐
│   │   ├── css 🎨              # CSS files for styling
│   │   ├── fonts 🅰️            # Font files used for the website
│   │   ├── images 🖼️           # Static images used for the website
│   │   ├── uploads 📤          # Folder to store uploaded files
│   │   └── watermarks 🌊       # Folder for the watermark templates
│   ├── templates 🧩
│   │   └── index.html 🖥️       # Main HTML template
│   ├── .env 🗃️                 # The enviroment variables file
│   ├── app.py 🐍               # The main Flask application script
│   ├── package-lock.json 🔒    # Lock file for npm dependencies (only for development)
│   ├── package.json 📄         # npm configuration file (only for development)
│   └── requirements.txt 📑     # List of Python dependencies
├── LICENSE 🏅                  # List of Python dependencies
└── README.md ℹ️           	    # The file you're reading now
```

## Requirements

Before running this project, you need to install the following:

- **LibreOffice (headless)**: This is required for converting `.docx` files to `.pdf` format. 

To install LibreOffice on Ubuntu, use the following command:
    
``` shell
sudo apt install libreoffice
```

- **Python environment**:

1. Create a virtual environment (venv) in the source directory:

``` shell
    python -m venv venv
```
    
2. Install the necessary dependencies:
    
``` shell
    pip install -r requirements.txt
```

- **npm (development only)**: Please note that npm is only used during development and is not required for deployment.

## Running the Application

Once you have installed all dependencies and set up the environment, you can run the application with the following command:

``` shell
    python app.py
```

This will start the Flask server locally. Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

## 👥 Made By

Vivere Filigrana was developed by:

<table>
	<tr>
		<th>Daniele Orazio Susino</th>      
	</tr>
	<tr>
		<td><img src="./resources/images/Daniele Orazio Susino.jpg" alt="Daniele Orazio Susino" width="150"></td>     
	</tr>
	<tr>
		<td>
			<a href="https://www.instagram.com/daniele.susino/">Instagram 📸</a><br>
			<a href="https://www.linkedin.com/in/susinodaniele/">LinkedIn 👔</a><br>
			<a href="mailto:susino.daniele@outlook.com">Email 📨</a>
		</td>
	</tr>
</table>


But was originally developed by:

- [GanciDev](https://www.linkedin.com/in/giuseppe-g/)
- [Ashenclock](https://www.instagram.com/ashenclock_/)

## License

This project is licensed under the GNU AGPL v3 license - see the [LICENSE](LICENSE) file for details.

### Major Limitations of the AGPL v3 License

1. **Use and Distribution**: You are free to use, modify, and distribute this software, provided that you adhere to the terms of the AGPL v3 license.

2. **Source Code Availability**: If you modify and deploy this software (e.g., as a web service), you must make the source code of the modified version available to the users of your service.

3. **No Commercial Use Without Source Disclosure**: If you use this software for commercial purposes, you must make the modified source code available under the same AGPL v3 license, ensuring that the same freedoms apply to any derivative works.

4. **Redistribution**: Any redistribution of the code, including modified versions, must also be licensed under the AGPL v3.

5. **Attribution**: When redistributing the software (modified or not), you must provide proper attribution to the original authors and indicate any changes made. You must also include the license text along with the redistribution.

For more detailed information, please refer to the [full AGPL v3 license](https://www.gnu.org/licenses/agpl-3.0.html).