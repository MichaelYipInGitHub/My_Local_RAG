main_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local RAG Solution</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            background-color: #2196f3;
            color: white;
            width: 100%;
            padding: 1.5em;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        main {
            margin: 2em;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            width: 90%;
            max-width: 800px;
            padding: 2em;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
            font-size: 1.1em;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            background-color: #2196f3;
            margin: 0.5em 0;
            padding: 1em;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        ul li a {
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        ul li:hover {
            background-color: #1976d2;
        }
        .material-icons {
            margin-right: 0.5em;
        }
    </style>
</head>
<body>
    <header>
        <h1>Local RAG Solution</h1>
    </header>
    <main>
        <p>If you need to directly interact with the model based on uploaded documents, please visit <a href="/chat">RAG Q&A</a>, upload files in the input box, and start the conversation. (The uploaded data will not be retained after refreshing the page. If you wish to persistently use and maintain the knowledge base, please create a knowledge base).</p>
        <p>If you need to create or update a knowledge base, follow the steps: <a href="/upload_data">Upload Data</a>, <a href="/create_knowledge_base">Create Knowledge Base</a>, and select the knowledge base you want to use in the "Load Knowledge Base" section of <a href="/chat">RAG Q&A</a>.</p>
        <p>If you need to perform Q&A based on an already created knowledge base, directly visit <a href="/chat">RAG Q&A</a> and select your created knowledge base in the "Load Knowledge Base" section.</p>
        <ul>
            <li><a href="/upload_data"><span class="material-icons"></span> 1. Upload Data</a></li>
            <li><a href="/create_knowledge_base"><span class="material-icons"></span> 2. Create Knowledge Base</a></li>
            <li><a href="/chat"><span class="material-icons"></span> 3. RAG Q&A</a></li>
        </ul>
    </main>
</body>
</html>"""

plain_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>RAG Q&A</title>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
        .links-container {
            display: flex;
            justify-content: center; /* Center the child elements in the container */
            list-style-type: none; /* Remove default list styling */
            padding: 0; /* Remove default padding */
            margin: 0; /* Remove default margin */
        }
        .links-container li {
            margin: 0 5px; /* Add some space around each li element */
            padding: 10px 15px; /* Add padding */
            border: 1px solid #ccc; /* Add border */
            border-radius: 5px; /* Add rounded corners */
            background-color: #f9f9f9; /* Background color */
            transition: background-color 0.3s; /* Transition effect for background color */
            display: flex; /* Use flex layout */
            align-items: center; /* Center vertically */
            height: 50px; /* Set fixed height for consistency */
        }
        .links-container li:hover {
            background-color: #e0e0e0; /* Background color on hover */
        }
        .links-container a {
            text-decoration: none !important; /* Remove underline from links */
            color: #333; /* Link color */
            font-family: Arial, sans-serif; /* Font */
            font-size: 14px; /* Font size */
            display: flex; /* Use flex layout */
            align-items: center; /* Center vertically */
            height: 100%; /* Ensure link height matches parent */
        }
        .material-icons {
            font-size: 20px; /* Icon size */
            margin-right: 8px; /* Space between icon and text */
            text-decoration: none; /* Ensure icons have no underline */
        }

        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            .links-container li {
                background-color: #333; /* Dark mode background color */
                border-color: #555; /* Dark mode border color */
            }
            .links-container li:hover {
                background-color: #555; /* Dark mode background color on hover */
            }
            .links-container a {
                color: #f9f9f9; /* Dark mode text color */
            }
        }
        </style>
    </head>
    <body>
        <ul class="links-container">
            <li><a href="/"><span class="material-icons">home</span> Home</a></li>
            <li><a href="/upload_data"><span class="material-icons">cloud_upload</span> Upload Data</a></li>
            <li><a href="/create_knowledge_base"><span class="material-icons">library_add</span> Create Knowledge Base</a></li>
            <li><a href="/chat"><span class="material-icons">question_answer</span> RAG Q&A</a></li>
        </ul>
    </body>
</html>"""