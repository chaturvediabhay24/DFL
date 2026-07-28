# DBMS Bulletin Board Project — Complete Viva Prep Guide

**Roll No:** MSc-DS-2025-10-0041 | **Course:** MDS301

---

## What Was Built

A **bulletin board web app** built in three progressive stages:

| Part | Tech | Marks | What Changed |
|------|------|-------|--------------|
| P1 | Python CGI + SQLite | 15 | Basic board: post, reply, search, edit, delete |
| P2 | Flask + SQLite | 15 | Same features, reimplemented in Flask |
| P3 | Flask + extended schema | 30 | Added users, tags, voting, 5 SQL queries |

**Viva = 30% of marks.** Be ready to explain every design decision.

---

## P1 — CGI Bulletin Board

### What is CGI?
CGI (Common Gateway Interface) is the old-school way to run server-side scripts. Each HTTP request spawns a new Python process. You run it with:
```bash
python3 -m http.server --cgi 8080
```
Every `.cgi` file is a standalone script that prints HTTP headers + HTML to stdout.

### Database Schema (P1)
```sql
CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    subject    VARCHAR(100) NOT NULL,
    sender     VARCHAR(15) NOT NULL,
    reply_to   INT,
    text       TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reply_to) REFERENCES messages(id)
);
```

**Key design points:**
- `reply_to` is a **self-referencing foreign key** — a message can reference another message as its parent. This is how threading works.
- `sender` is just a plain string (no authentication in P1).
- `created_at` uses `DEFAULT CURRENT_TIMESTAMP` so SQLite fills it automatically.
- `AUTOINCREMENT` ensures IDs never reuse deleted values.

### Files in P1
| File | Purpose |
|------|---------|
| `schema.sql` | Creates the messages table |
| `db.py` | Shared DB connection helper |
| `cgi-bin/main.cgi` | Homepage — shows all messages in thread tree |
| `cgi-bin/addmessage.cgi` | Form to post new message or reply |
| `cgi-bin/search.cgi` | Search by subject/sender |
| `cgi-bin/edit.cgi` | Edit a message (checks sender name) |
| `cgi-bin/delete.cgi` | Delete a message (checks sender name) |

### db.py Pattern (used in all 3 parts)
```python
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # lets you do row['column_name']
    conn.execute("PRAGMA foreign_keys = ON")  # SQLite disables FK by default!
    return conn
```

**IMPORTANT:** SQLite does NOT enforce foreign keys by default. You must run `PRAGMA foreign_keys = ON` every connection.

### How Threading Works
- Top-level messages have `reply_to = NULL`
- Replies have `reply_to = <parent_id>`
- To display threads: fetch all top-level messages, then recursively fetch replies to each

### Ownership Verification in P1
No real auth. When editing/deleting, the user must type the sender name again. The code checks:
```python
if sender_input == message['sender']:
    # allow edit/delete
```
Weakness: anyone who knows your name can edit your posts.

---

## P2 — Flask Reimplementation

### What Changed from P1?
- **Same database schema** — no changes to `schema.sql`
- Replaced CGI scripts with Flask routes
- Used Jinja2 templates with template inheritance (base.html)
- Cleaner URL structure (`/post`, `/edit/<id>`, `/delete/<id>`)

### Flask Route Map
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Show all messages (threaded) |
| `/post` | GET/POST | Post new message or reply |
| `/search` | GET | Search messages |
| `/edit/<id>` | GET/POST | Edit a message |
| `/delete/<id>` | POST | Delete a message |

### The `get_message_tree()` Function
This is the core of threading — understand it well:
```python
def get_message_tree(msg_id, conn):
    msg = conn.execute("SELECT * FROM messages WHERE id=?", (msg_id,)).fetchone()
    replies = conn.execute(
        "SELECT * FROM messages WHERE reply_to=? ORDER BY created_at ASC", (msg_id,)
    ).fetchall()
    return {
        'msg': msg,
        'replies': [get_message_tree(r['id'], conn) for r in replies]  # recursion
    }
```
It builds a nested dictionary tree using **recursion (DFS)**. The Jinja2 template then recursively renders this tree with indentation.

### Template Inheritance (Jinja2)
- `base.html` — has `{% block content %}{% endblock %}` 
- All other templates do `{% extends 'base.html' %}` and fill the block
- Avoids repeating CSS, navigation, error display across files

### Parameterized Queries — Always!
```python
# CORRECT — parameterized (safe from SQL injection)
conn.execute("SELECT * FROM messages WHERE id=?", (msg_id,))

# WRONG — string formatting (SQL injection risk)
conn.execute(f"SELECT * FROM messages WHERE id={msg_id}")
```
Every query in this project uses `?` placeholders. This is non-negotiable.

---

## P3 — Extended Schema: Users, Tags, Votes

### What Changed from P2?
1. `sender` string field → `sender_id` FK to a `users` table
2. Added `tags` table and `message_tags` join table
3. Added `votes` table
4. Added Flask sessions for login
5. Added `/stats` page with 5 queries

### Full Schema (P3)
```sql
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    subject    VARCHAR(100) NOT NULL,
    sender_id  INT NOT NULL,                        -- FK, not a string anymore
    reply_to   INT,
    text       TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (reply_to)  REFERENCES messages(id)
);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS message_tags (
    message_id INT NOT NULL,
    tag_id     INT NOT NULL,
    PRIMARY KEY (message_id, tag_id),               -- composite PK prevents duplicates
    FOREIGN KEY (message_id) REFERENCES messages(id),
    FOREIGN KEY (tag_id)     REFERENCES tags(id)
);

CREATE TABLE IF NOT EXISTS votes (
    user_id    INT NOT NULL,
    message_id INT NOT NULL,
    vote_value INT NOT NULL CHECK (vote_value IN (-1, 1)),  -- only +1 or -1
    PRIMARY KEY (user_id, message_id),              -- one vote per user per message
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (message_id) REFERENCES messages(id)
);
```

### Why Each Table Exists

**`users`** — Normalizes user identity. In P1/P2, same person could post as "Alice" and "alice" — now username is UNIQUE.

**`message_tags`** — Tags-to-messages is many-to-many (a message can have multiple tags, a tag can be on multiple messages). You can't store this in either table directly — you need a **junction/join table**.

**`votes`** — Composite PK `(user_id, message_id)` ensures one vote per user per message at the database level, not just in code.

### Login Flow (Auto-Registration)
```python
user = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
if not user:
    conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
session['user_id'] = user['id']
session['username'] = username
```
No passwords. First time you type a username → account created. After that, same username = same user. Session stores user_id in a signed cookie.

### Voting Logic (Important!)
Three cases when user clicks +1 or -1:
1. **No existing vote** → INSERT new vote
2. **Existing vote, same value** → DELETE (toggle off)
3. **Existing vote, different value** → UPDATE to new value

```python
existing = conn.execute(
    "SELECT vote_value FROM votes WHERE user_id=? AND message_id=?",
    (session['user_id'], msg_id)
).fetchone()

if existing:
    if existing['vote_value'] == vote_value:
        conn.execute("DELETE FROM votes WHERE user_id=? AND message_id=?", ...)
    else:
        conn.execute("UPDATE votes SET vote_value=? WHERE user_id=? AND message_id=?", ...)
else:
    conn.execute("INSERT INTO votes (user_id, message_id, vote_value) VALUES (?, ?, ?)", ...)
```

### Tag Management
User types tags as comma-separated string in the form. Code splits, trims, and upserts:
```python
for tag_name in tags_str.split(','):
    tag_name = tag_name.strip()
    tag = conn.execute("SELECT id FROM tags WHERE name=?", (tag_name,)).fetchone()
    if not tag:
        conn.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
        tag = conn.execute("SELECT id FROM tags WHERE name=?", (tag_name,)).fetchone()
    conn.execute("INSERT INTO message_tags (message_id, tag_id) VALUES (?, ?)", (msg_id, tag['id']))
```

### Cascade Delete in P3
When deleting a message, must clean up votes and tags first (SQLite doesn't auto-cascade):
```python
conn.execute("DELETE FROM votes WHERE message_id IN (SELECT id FROM messages WHERE reply_to=? OR id=?)", (msg_id, msg_id))
conn.execute("DELETE FROM message_tags WHERE message_id IN (SELECT id FROM messages WHERE reply_to=? OR id=?)", (msg_id, msg_id))
conn.execute("DELETE FROM messages WHERE reply_to=?", (msg_id,))
conn.execute("DELETE FROM messages WHERE id=?", (msg_id,))
```
Order matters: delete from child tables before parent table.

---

## The 5 Required SQL Queries (P3) — Know These Cold

### Query 1: Top 5 Most Upvoted Messages
```sql
SELECT
    m.id, m.subject, u.username, m.created_at,
    COALESCE(SUM(v.vote_value), 0) AS net_votes
FROM messages m
LEFT JOIN users u ON m.sender_id = u.id
LEFT JOIN votes v ON m.id = v.message_id
GROUP BY m.id
ORDER BY net_votes DESC
LIMIT 5;
```
**Why LEFT JOIN?** If a message has no votes, INNER JOIN would exclude it. LEFT JOIN keeps it with NULL, then COALESCE turns NULL → 0.

**Why GROUP BY m.id?** SUM aggregates all vote rows per message — need GROUP BY to do this per-message.

### Query 2: Messages Per Tag
```sql
SELECT
    t.name,
    COUNT(DISTINCT mt.message_id) AS message_count
FROM tags t
LEFT JOIN message_tags mt ON t.id = mt.tag_id
GROUP BY t.id, t.name
ORDER BY message_count DESC;
```
**Why DISTINCT?** Prevents double-counting if a message appears multiple times in the join.

**Why LEFT JOIN?** Includes tags that have zero messages.

### Query 3: Most Active Users (Top 5)
```sql
SELECT
    u.username,
    COUNT(m.id) AS message_count
FROM users u
LEFT JOIN messages m ON u.id = m.sender_id
GROUP BY u.id, u.username
ORDER BY message_count DESC
LIMIT 5;
```
**Why LEFT JOIN?** Includes users who have never posted (count = 0).

### Query 4: Threads with Most Replies (Top 5)
```sql
SELECT
    m.id, m.subject, u.username,
    COUNT(r.id) AS reply_count
FROM messages m
LEFT JOIN users u ON m.sender_id = u.id
LEFT JOIN messages r ON m.id = r.reply_to  -- self-join to find replies
WHERE m.reply_to IS NULL                    -- only top-level messages
GROUP BY m.id
ORDER BY reply_count DESC
LIMIT 5;
```
**Why self-join?** We join the messages table with itself to find messages (`r`) whose `reply_to` equals the top-level message's id.

**Why WHERE m.reply_to IS NULL?** Filters to only original posts, not replies-to-replies.

### Query 5: Users Who Have Never Voted
```sql
SELECT u.id, u.username
FROM users u
WHERE u.id NOT IN (SELECT DISTINCT user_id FROM votes);
```
**Alternative using LEFT JOIN:**
```sql
SELECT u.id, u.username
FROM users u
LEFT JOIN votes v ON u.id = v.user_id
WHERE v.user_id IS NULL;
```
Both approaches are valid. The subquery version is more readable.

---

## Common Viva Questions — With Answers

### Database Design

**Q: Why did sender go from a string to a foreign key in P3?**
A: In P1/P2, the same person could post as "alice" and "Alice" — two different identities. Using a foreign key to a users table enforces a single identity per user. It also avoids data redundancy (username stored once in users, not repeated in every message).

**Q: What is a composite primary key? Where is it used?**
A: A primary key made of two or more columns. Used in `message_tags (message_id, tag_id)` and `votes (user_id, message_id)`. Prevents inserting duplicate combinations — enforces "one vote per user per message" at the DB level.

**Q: What is a self-referencing foreign key?**
A: A foreign key that references the same table. In `messages`, `reply_to` references `messages(id)`. This models hierarchical/tree structures within one table.

**Q: What does PRAGMA foreign_keys = ON do?**
A: SQLite doesn't enforce foreign key constraints by default for backward compatibility. This PRAGMA turns enforcement on for the current connection.

**Q: Why is `vote_value CHECK (vote_value IN (-1, 1))` there?**
A: It's a check constraint — a rule the DB enforces. Without it, code could insert any integer. With it, the DB rejects anything that isn't -1 or 1.

**Q: What's the difference between INNER JOIN and LEFT JOIN?**
A: INNER JOIN returns only rows where the join condition matches in BOTH tables. LEFT JOIN returns ALL rows from the left table, with NULLs for the right table when there's no match. We use LEFT JOIN when we want to include records with no related data (e.g., messages with no votes).

**Q: What does COALESCE do?**
A: `COALESCE(expr, default)` returns the first non-NULL value. `COALESCE(SUM(v.vote_value), 0)` returns 0 if SUM is NULL (i.e., no votes exist).

### Application Logic

**Q: How does threading work?**
A: Each message has a `reply_to` field. Top-level messages have `reply_to = NULL`. Replies have `reply_to = <parent_id>`. A recursive function (`get_message_tree`) fetches a message and all its replies, building a nested structure. The template renders this with indentation.

**Q: How is authentication done in P3?**
A: Lightweight session-based auth. User types a username → if it exists, they're logged in; if not, account is created automatically. The `user_id` and `username` are stored in a Flask session (signed cookie). Every protected route checks `session.get('user_id')`.

**Q: Why use sessions instead of URL parameters for authentication?**
A: URL parameters are visible in browser history, logs, and can be shared accidentally. Sessions store the auth token in a cookie, which is sent automatically and not visible in the URL.

**Q: How do you prevent SQL injection?**
A: Use parameterized queries with `?` placeholders. Never use string concatenation or f-strings to build SQL queries. The DB driver handles escaping.

**Q: What is the ownership check in P3?**
A: When editing/deleting, code checks `message['sender_id'] == session['user_id']`. If they don't match, the operation is rejected. In P3 this uses actual user IDs (secure); in P1/P2 it used string matching (anyone knowing your name could impersonate you).

**Q: What happens when you delete a message in P3?**
A: Must delete in this order: votes on replies → message_tags on replies → replies → votes on the message → message_tags of the message → the message itself. This avoids FK constraint violations.

### Query Explanation

**Q: Explain Query 4 (threads with most replies) — why is it a self-join?**
A: We need to count how many messages have `reply_to = m.id`. This means we join the messages table with itself — aliased as `m` (parents) and `r` (replies). `LEFT JOIN messages r ON m.id = r.reply_to` matches each parent message to all its direct replies, then COUNT(r.id) gives the reply count.

**Q: What's the difference between WHERE and HAVING in a GROUP BY query?**
A: WHERE filters rows BEFORE grouping. HAVING filters groups AFTER aggregation. Example: `HAVING COUNT(m.id) > 5` would filter users with more than 5 messages — this can't be done with WHERE.

---

## Architecture Summary

```
P1:  Browser → HTTP Server → CGI Script → SQLite DB
P2:  Browser → Flask App → SQLite DB
P3:  Browser → Flask App (with sessions) → SQLite DB (5 tables)
```

**File structure (P3):**
```
P3/
├── app.py          # Flask routes and business logic
├── db.py           # DB connection, init, helper functions
├── schema.sql      # Table definitions
├── queries.sql     # The 5 required SQL queries
└── templates/
    ├── base.html   # Common layout, navigation
    ├── login.html  # Username form
    ├── board.html  # Main board + voting
    ├── post.html   # Post/reply form
    ├── edit.html   # Edit form with tags
    └── search.html # Search results
```

---

## Quick Reference: Schema Relationships

```
users (id, username)
  |
  |-- messages (id, subject, sender_id→users, reply_to→messages, text, created_at)
  |                |
  |                |-- message_tags (message_id→messages, tag_id→tags)
  |                |                              |
  |                |                           tags (id, name)
  |                |
  |-- votes (user_id→users, message_id→messages, vote_value)
```

---

## Things to Practice Saying Out Loud

1. "The `reply_to` column is a self-referencing foreign key that enables threaded discussions."
2. "We use LEFT JOIN instead of INNER JOIN to include messages/users that have no associated votes/tags."
3. "COALESCE handles the NULL case when there are no votes — it returns 0 instead of NULL."
4. "The composite primary key on votes ensures one vote per user per message at the database level."
5. "We use parameterized queries with `?` placeholders to prevent SQL injection."
6. "PRAGMA foreign_keys = ON is required because SQLite doesn't enforce foreign keys by default."
7. "Cascade deletion must be done manually in SQLite — delete from child tables before parent."
8. "Tags are many-to-many with messages, so we need a junction table `message_tags`."
