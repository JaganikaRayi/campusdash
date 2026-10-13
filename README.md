# 🎓 CampusDash – Smart Campus Management System
> **Python మరియు Advanced Data Structures & Algorithms (ADS) ఆధారిత స్మార్ట్ క్యాంపస్ మేనేజ్‌మెంట్ సిస్టమ్**

---

## 🌟 ప్రాజెక్ట్ పరిచయం (Project Overview)
**CampusDash** అనేది కాలేజ్ విద్యార్థులు (Students), అధ్యాపకులు (Faculty), మరియు అడ్మినిస్ట్రేటర్ల (Administrators) కోసం రూపొందించబడిన ఆధునిక వెబ్ అప్లికేషన్. 
ఇందులో కేవలం సాధారణ CRUD ఆపరేషన్లు మాత్రమే కాకుండా, కంప్యూటర్ సైన్స్‌లోని **9 వాస్తవ అడ్వాన్స్‌డ్ డేటా స్ట్రక్చర్స్ మరియు అల్గారిథమ్స్ (ADS)** నేరుగా సిస్టమ్ ఫీచర్లకు అనుసంధానించబడి పనిచేస్తాయి.

---

## 🛠️ టెక్నాలజీ స్టాక్ (Technology Stack)
- **ఫ్రంట్‌ఎండ్ (Frontend)**: HTML5, CSS3 (Modern Glassmorphic UI), JavaScript (ES6+ Fetch API), Bootstrap 5, FontAwesome, Chart.js
- **బ్యాకెండ్ (Backend)**: Python 3, Flask REST API, Flask-CORS
- **డేటాబేస్ (Database)**: SQLite (జీరో-కాన్ఫిగరేషన్, ఆటోమేటిక్ టేబుల్స్ క్రియేషన్ & డెమో డేటా సీడింగ్)
- **అల్గారిథమ్స్ (ADS Engine)**: Hash Table, Binary Search, Graph (BFS & Dijkstra), Greedy Scheduling, Backtracking, Merge Sort, FIFO Queue, Priority Queue Heap, Dynamic Programming (0/1 Knapsack)

---

## 🚀 ప్రాజెక్ట్ రన్ చేయడానికి స్టెప్-బై-స్టెప్ గైడ్ (Beginner-Friendly Setup Guide in Telugu)

### 1️⃣ పైథాన్ చెక్ చేయండి (Python Installation Check)
మీ కంప్యూటర్‌లో పైథాన్ ఇన్‌స్టాల్ అయి ఉందో లేదో చూడటానికి టెర్మినల్ లేదా పవర్‌షెల్ (PowerShell) లో క్రింది కమాండ్ రన్ చేయండి:
```powershell
python --version
```
*(కనిష్టంగా Python 3.9 లేదా అంతకంటే ఎక్కువ వెర్షన్ ఉండాలి)*

---

### 2️⃣ VS Code లో ప్రాజెక్ట్ ఫోల్డర్ ఓపెన్ చేయండి (Open Folder in VS Code)
1. Visual Studio Code ఓపెన్ చేయండి.
2. `File` -> `Open Folder` క్లిక్ చేసి, మీ సిస్టమ్‌లోని `CampusDash` ఫోల్డర్‌ను ఎంచుకోండి.
3. కీబోర్డులో `Ctrl + ~` ప్రెస్ చేసి టెర్మినల్ (Integrated Terminal) ఓపెన్ చేయండి.

---

### 3️⃣ వర్చువల్ ఎన్విరాన్‌మెంట్ తయారు చేయండి (Create Virtual Environment)
విండోస్ (Windows) లో ప్రాజెక్ట్ ఐసొలేషన్ కోసం వర్చువల్ ఎన్విరాన్‌మెంట్‌ను క్రియేట్ చేసి యాక్టివేట్ చేయండి:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
*(గమనిక: యాక్టివేట్ అయినప్పుడు మీ ప్రాంప్ట్ ముందు `(.venv)` అని కనిపిస్తుంది)*

---

### 4️⃣ లైబ్రరీలు ఇన్‌స్టాల్ చేయండి (Install Requirements)
క్రింది కమాండ్‌తో Flask మరియు Flask-CORS లైబ్రరీలను ఇన్‌స్టాల్ చేయండి:
```powershell
python -m pip install -r requirements.txt
```

---

### 5️⃣ ప్రాజెక్ట్ సర్వర్‌ను ప్రారంభించండి (Run Flask Server)
```powershell
python app.py
```
ఈ కమాండ్ రన్ చేసిన వెంటనే:
1. SQLite డేటాబేస్ (`instance/campusdash.db`) ఆటోమేటిక్‌గా క్రియేట్ అవుతుంది.
2. టేబుల్స్ మరియు `25221A0501` నుండి `25221A05F4` వరకు డెమో విద్యార్థులు, ఫ్యాకల్టీ, టైమ్‌టేబుల్, ఫీజు రికార్డులు ఆటోమేటిక్‌గా ఫీడ్ అవుతాయి.

---

### 6️⃣ బ్రౌజర్‌లో అప్లికేషన్ ఓపెన్ చేయండి (Open in Browser)
మీ Chrome లేదా Edge బ్రౌజర్‌ను ఓపెన్ చేసి క్రింది అడ్రస్‌ను ఎంటర్ చేయండి:
```text
http://127.0.0.1:5000
```

---

## 🔑 డెమో లాగిన్ వివరాలు (Demo Login Credentials)

| యూజర్ రోల్ (Role) | యూజర్‌నేమ్ (Username / ID) | పాస్‌వర్డ్ (Password / Name) | ఉపయోగాలు |
|---|---|---|---|
| **Student (విద్యార్థి)** | `25221A0501` | `Aarav Reddy` (లేదా `student123`) | హాజరు, టైమ్‌టేబుల్, ఫీజు చెల్లింపు, ఫలితాలు, లీవ్ దరఖాస్తు |
| **Faculty (అధ్యాపకులు)** | `FAC01` | `faculty123` | పీరియడ్-వైజ్ హాజరు వేయడం, క్లాస్ నివేదికలు, స్టడీ మెటీరియల్ |
| **Administrator (అడ్మిన్)** | `admin` | `admin123` | మొత్తం కాలేజ్ వివరాలు, ఫీజు కలెక్షన్స్, లీవ్ ఆమోదం, టైమ్‌టేబుల్ |

*(సూచన: లాగిన్ పేజీలో **Quick 1-Click Demo Login** బటన్స్ ఉన్నాయి. వాటిని క్లిక్ చేస్తే ఆటోమేటిక్‌గా క్రెడెన్షియల్స్ ఫిల్ అవుతాయి!)*

---

## 🧠 ఇందులో ఉన్న 9 ADS అల్గారిథమ్స్ వివరణ (Explanation of ADS Algorithms)

### 1. Hash Table / Dictionary Lookups (Algorithm 1)
- **ఉపయోగం**: విద్యార్థి రిజిస్ట్రేషన్ నంబర్ (`25221A0501`) తో విద్యార్థి వివరాలను వెతకడం.
- **టైమ్ కాంప్లెక్సిటీ**: **O(1)** సగటు సమయం.
- **ఎందుకు ప్రత్యేకం?**: వేల సంఖ్యలో విద్యార్థులు ఉన్నా, కంప్యూటర్ ఒక్క స్టెప్‌లోనే నేరుగా హాష్ బకెట్ ద్వారా రికార్డును చేరుకుంటుంది.

### 2. Binary Search (Algorithm 2)
- **ఉపయోగం**: సార్ట్ చేయబడిన రోల్ నంబర్ల జాబితాలో డివైడ్ అండ్ కాంకర్ (Divide and Conquer) పద్ధతిలో సెర్చ్ చేయడం.
- **టైమ్ కాంప్లెక్సిటీ**: **O(log n)**.
- **పోలిక**: లీనియర్ సెర్చ్ 60 కంపారిజన్లు తీసుకుంటే, బైనరీ సెర్చ్ కేవలం 5 నుండి 6 స్టెప్పులలోనే కనుగొంటుంది.

### 3. Graph Algorithms – BFS & Dijkstra (Algorithm 3)
- **ఉపయోగం**: స్మార్ట్ క్యాంపస్ నావిగేషన్ (Campus Navigation Route Finder).
- **BFS (Breadth-First Search)**: క్యాంపస్‌లోని బిల్డింగులను లేయర్ల వారీగా ఎక్స్‌ప్లోర్ చేస్తుంది (Hop-level traversal).
- **Dijkstra's Algorithm**: ప్రధాన గేట్ నుండి CSE బ్లాక్ లేదా లైబ్రరీకి అతి తక్కువ నడక దూరం (Shortest walking path in meters) ను కనుగొంటుంది.

### 4. Greedy Timetable Scheduling (Algorithm 4)
- **ఉపయోగం**: తరగతులకు లెక్చరర్లు మరియు గదులను మొదట ఖాళీగా ఉన్న పీరియడ్‌కు కేటాయించడం.
- **పరిమితి**: తక్కువ గదులు ఉన్నప్పుడు గ్రీడీ విధానం క్లాష్ (Conflict) లను కలిగిస్తుంది.

### 5. Backtracking Timetable Scheduling (Algorithm 5)
- **ఉపయోగం**: 100% క్లాష్-ఫ్రీ (Clash-Free) టైమ్‌టేబుల్ జనరేషన్.
- **పనిచేసే విధానం**: ఏదైనా పీరియడ్‌లో ఫ్యాకల్టీ లేదా రూమ్ కాన్‌ఫ్లిక్ట్ ఏర్పడితే, వెనక్కి వెళ్లి (Backtrack) ప్రత్యామ్నాయ స్లాట్‌లను వెతికి సరైన షెడ్యూల్‌ను రూపొందిస్తుంది.

### 6. Merge Sort (Algorithm 6)
- **ఉపయోగం**: విద్యార్థుల అటెండెన్స్ పర్సంటేజ్ లేదా రిజిస్ట్రేషన్ నంబర్ల ఆధారంగా ర్యాంకింగ్ సార్ట్ చేయడం.
- **టైమ్ కాంప్లెక్సిటీ**: స్థిరమైన **O(n log n)**.

### 7. Queue – FIFO (Algorithm 7)
- **ఉపయోగం**: విద్యార్థులు సమర్పించిన లీవ్ దరఖాస్తులను వారు దరఖాస్తు చేసిన సమయ క్రమం (First-Come, First-Served) లో ప్రాసెస్ చేయడం.

### 8. Priority Queue / Binary Max-Heap (Algorithm 8)
- **ఉపయోగం**: అత్యవసర మెడికల్ లీవ్ అభ్యర్థనలు మరియు అత్యవసర నోటిఫికేషన్లను ముందు వరుసలో ఉంచి వేగంగా పరిష్కరించడం (Urgent Priority 3 > Academic 2 > Personal 1).

### 9. Dynamic Programming – 0/1 Knapsack Study Planner (Algorithm 9)
- **సమస్య**: పరీక్షల ముందు విద్యార్థి వద్ద పరిమిత సమయం (ఉదాహరణకు 8 గంటలు) మాత్రమే ఉన్నప్పుడు, ఏయే సిలబస్ టాపిక్స్ చదివితే అత్యధిక మార్కులు (Max Exam Score) సాధించవచ్చో ఎంచుకోవడం.
- **ఫలితం**: DP మ్యాట్రిక్స్ ద్వారా గరిష్ట మార్కులు తెచ్చే సరైన టాపిక్స్ కాంబినేషన్‌ను లెక్కిస్తుంది.

---

## 📂 ఫోల్డర్ల అమరిక (Project Directory Structure)
```text
CampusDash/
├── app.py                      # ప్రధాన ఫ్లాస్క్ అప్లికేషన్ & ఆటో డీబీ ఇనిషియలైజేషన్
├── config.py                   # కాన్ఫిగరేషన్ సెట్టింగులు
├── requirements.txt            # పైథాన్ డిపెండెన్సీలు
├── README.md                   # పూర్తి ప్రాజెక్ట్ వివరణ & గైడ్ (తెలుగులో)
├── database/
│   ├── schema.sql              # రిలేషనల్ టేబుల్స్ స్కీమా
│   └── db.py                   # డేటాబేస్ కనెక్షన్ & డెమో డేటా సీడింగ్
├── instance/
│   └── campusdash.db           # ఆటోమేటిక్‌గా క్రియేట్ అయ్యే SQLite డేటాబేస్
├── backend/
│   ├── algorithms/             # 9 ADS అల్గారిథమ్స్ పైథాన్ మోడ్యూల్స్
│   │   ├── searching.py        # Hash Table, Binary Search, Linear Search
│   │   ├── sorting.py          # Merge Sort
│   │   ├── graph_algorithms.py # BFS & Dijkstra
│   │   ├── greedy.py           # Greedy Timetable
│   │   ├── backtracking.py     # Backtracking Constraint Scheduler
│   │   ├── queues.py           # FIFO Queue & Priority Queue Heap
│   │   └── dynamic_programming.py # 0/1 Knapsack Study Planner
│   ├── routes/                 # REST API బ్లూప్రింట్స్
│   │   ├── auth.py, students.py, attendance.py, fees.py, timetable.py, academic.py, algorithms.py
│   └── services/               # బిజినెస్ లాజిక్ సర్వీసులు
├── frontend/                   # రెస్పాన్సివ్ UI పేజీలు
│   ├── index.html              # లాండింగ్ & లాగిన్ పేజీ
│   ├── dashboard.html          # మెయిన్ డాష్‌బోర్డ్
│   ├── attendance.html         # పీరియడ్-వైజ్ అటెండెన్స్
│   ├── fees.html               # ఫీజు & ఈ-రసీదులు
│   ├── timetable.html          # వీక్లీ టైమ్‌టేబుల్
│   ├── results.html            # ఎగ్జామ్ ఫలితాలు & SGPA
│   ├── materials.html          # స్టడీ మెటీరియల్స్
│   ├── faculty.html            # అధ్యాపకుల వివరాలు
│   ├── notifications.html      # నోటిఫికేషన్లు
│   ├── leave.html              # లీవ్ మేనేజ్‌మెంట్
│   ├── algorithms.html         # లైవ్ ADS విజువలైజర్ సూట్
│   ├── css/style.css           # మోడ్రన్ గ్లాస్‌మార్ఫిక్ స్టైలింగ్
│   └── js/                     # క్లయింట్-సైడ్ లాజిక్ (api.js, auth.js, algorithms.js...)
└── tests/
    ├── test_algorithms.py      # అల్గారిథమ్స్ యూనిట్ టెస్టులు (8/8 పాస్)
    └── test_api.py             # REST API ఎండ్‌పాయింట్ టెస్టులు (4/4 పాస్)
```

---

## ❓ తరచుగా వచ్చే సందేహాలు & పరిష్కారాలు (Troubleshooting Common Errors)

1. **`python : The term 'python' is not recognized`**:
   - మీ సిస్టమ్ ఎన్విరాన్‌మెంట్ వేరియబుల్స్ (PATH) లో పైథాన్ పాత్ యాడ్ చేయబడిందో లేదో చూడండి. విండోస్‌లో Python రీఇన్‌స్టాల్ చేసేటప్పుడు **"Add Python to PATH"** టిక్ మార్క్ పెట్టండి.
2. **`Address already in use` (Port 5000 Error)**:
   - వేరే ప్రాసెస్ పోర్ట్ 5000 ను వాడుతుంటే, `app.py` లో పోర్ట్‌ను 5050 లేదా 8000 గా మార్చి రన్ చేయవచ్చు:
     `flask run --port 5050`
3. **డేటాబేస్ రీసెట్ చేయాలంటే?**:
   - `instance/campusdash.db` ఫైల్‌ను డిలీట్ చేసి `python app.py` ను మళ్లీ రన్ చేస్తే, సరికొత్త ఫ్రెష్ డేటాబేస్ ఆటోమేటిక్‌గా సీడ్ అవుతుంది.

---

## 🎯 వైవా & ప్రాజెక్ట్ రివ్యూ టిప్స్ (Viva Presentation Tips)
- ఎగ్జామినర్ ముందు బ్రౌజర్‌లో **`ADS Visualizer (algorithms.html)`** పేజీని ఓపెన్ చేయండి.
- **Search Tab** లో ఏదైనా రోల్ నంబర్ కొట్టి, హాష్ టేబుల్ ఎలా **1 operation** లో రిజల్ట్ ఇచ్చిందో, లీనియర్ సెర్చ్ ఎన్ని కంపారిజన్లు తీసుకుందో గ్రాఫికల్‌గా చూపించండి.
- **Timetable Tab** లో గ్రీడీ షెడ్యూలర్ క్లాష్‌లను ఎలా చూపిస్తుందో, బ్యాక్‌ట్రాకింగ్ అల్గారిథమ్ వెనక్కి వెళ్లి ఆ క్లాష్‌లను ఎలా నివారిస్తుందో ప్రదర్శించండి!
