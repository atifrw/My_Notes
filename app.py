<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TranscribeYT - Professional YouTube Transcript Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
        }

        /* Navbar */
        nav {
            padding: 1.5rem 10%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }

        /* Hero Section */
        .hero {
            padding: 80px 10%;
            text-align: center;
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #0f172a;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 2rem;
        }

        /* Main Container */
        .container {
            max-width: 800px;
            margin: -50px auto 50px;
            padding: 0 20px;
        }

        .main-card {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            border-color: var(--primary-color);
        }

        .btn-primary {
            background-color: var(--primary-color);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        .btn-primary:hover {
            background-color: var(--secondary-color);
        }

        /* Transcript Result Area */
        .result-area {
            display: none; /* Default hidden */
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 30px;
        }

        .transcript-box {
            background: #f1f5f9;
            padding: 20px;
            border-radius: 8px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-size: 0.95rem;
            text-align: left;
        }

        .copy-btn {
            margin-top: 15px;
            background: #64748b;
            color: white;
            padding: 8px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        footer {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

    <nav>
        <div class="logo">TranscribeYT</div>
        <div>
            <a href="#" style="text-decoration: none; color: var(--text-muted); font-weight: 500;">Features</a>
        </div>
    </nav>

    <header class="hero">
        <h1>YouTube Video to <span style="color: var(--primary-color);">Transcript</span></h1>
        <p>Kisi bhi YouTube video ka URL paste karein aur uska pura text (transcript) turant payein.</p>
    </header>

    <div class="container">
        <div class="main-card">
            <div class="input-group">
                <input type="text" id="videoUrl" placeholder="Paste YouTube Link here (e.g., https://youtube.com/...)">
                <button class="btn-primary" onclick="generateTranscript()">Get Transcript</button>
            </div>

            <div id="resultSection" class="result-area">
                <h3 style="margin-bottom: 15px;">Transcript Output:</h3>
                <div id="transcriptOutput" class="transcript-box">
                    Processing your video... Please wait.
                </div>
                <button class="copy-btn" onclick="copyText()">Copy Text</button>
            </div>
        </div>
    </div>

    <footer>
        &copy; 2024 TranscribeYT - Made for Content Creators
    </footer>

    <script>
        function generateTranscript() {
            const url = document.getElementById('videoUrl').value;
            if(!url) {
                alert("Please paste a valid YouTube URL");
                return;
            }

            // UI change to show loading
            document.getElementById('resultSection').style.display = 'block';
            document.getElementById('transcriptOutput').innerText = "Loading transcript for: " + url + "\n\n(Note: Yahan backend API link karni hogi transcript fetch karne ke liye.)";
        }

        function copyText() {
            const text = document.getElementById('transcriptOutput').innerText;
            navigator.clipboard.writeText(text);
            alert("Transcript copied to clipboard!");
        }
    </script>
</body>
</html>
