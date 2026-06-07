<div dir="rtl">

# אפליקציית חיזוי דירוג סרטים

**שם:** רועי אשכנזי  
**פרויקט:** מטלת סיכום — חלק 3  
**קורס:** למידת מכונה

---

## תיאור הפרויקט

בניתי אפליקציית ווב המאפשרת לחזות את הדירוג הממוצע של סרט ב-IMDb.  
האפליקציה עוטפת את מודל ה-Random Forest שפיתחתי בחלק 2 של הפרויקט.  
המשתמש מכניס פרמטרים של סרט (שנת יציאה, אורך, ז'אנרים וכו'), לוחץ על כפתור Predict Rating — והדף מציג את התחזית מיידית ללא רענון.

---

## מבנה הקבצים

<div dir="ltr">

| File | Description |
|------|-------------|
| `api.py` | שרת Flask — מטפל בבקשות ומחזיר תחזיות |
| `index.html` | ממשק המשתמש — טופס קלט והצגת תוצאה |
| `assets_data_prep.py` | פונקציית `prepare_data()` — הנדסת פיצ'רים |
| `trained_model.pkl` | המודל המאומן מחלק 2 |
| `requirements.txt` | כל הספריות הנדרשות עם גרסאותיהן |

</div>

---

## הוראות התקנה

**שלב 1 — שכפול הפרויקט:**

<div dir="ltr">

```bash
git clone https://github.com/RoidoAsh/movie_rating_app.git
cd movie_rating_app
```

</div>

**שלב 2 — יצירת סביבה וירטואלית והפעלתה:**

<div dir="ltr">

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

</div>

**שלב 3 — התקנת הספריות:**

<div dir="ltr">

```bash
pip install -r requirements.txt
```

</div>

---

## הוראות הפעלה

<div dir="ltr">

```bash
python api.py
```

</div>

לאחר ההרצה, פותחים דפדפן וניגשים לכתובת:

<div dir="ltr">

```
http://localhost:5000
```

</div>

---

## שדות הקלט וטווחי הערכים

<div dir="ltr">

| Field | Description | Range / Example |
|-------|-------------|-----------------|
| Movie Title | שם הסרט | טקסט חופשי |
| Release Year | שנת יציאה | 1900 – 2030 |
| Runtime | אורך הסרט בדקות | 1 – 600 |
| Budget | תקציב הסרט | e.g. $10 million |
| Number of Lead Actors | מספר שחקנים מובילים | 0 – 5 |
| Country | מדינת הפקה | e.g. United States |
| Language | שפת הסרט | e.g. English |
| Genres | ז'אנרים | בחירה מתוך 10 אפשרויות |
| Plot Summary | האם קיים תקציר עלילה | Yes / No |

</div>

**שים לב:** השדות Release Year ו-Runtime הם שדות חובה. שאר השדות אופציונליים.

---

## הערות

- המודל אומן על נתוני IMDb של כ-133,000 סרטים
- טווח הדירוגים הוא 1–10
- התחזית מדויקת יותר ככל שממלאים יותר שדות

</div>
