import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_posts():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posts(posts):
    with open('data.json', 'w') as f:
        json.dump(posts, f, indent=4)

def get_post_by_id(posts, post_id):
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        posts = load_posts()
        new_id = 1
        if posts:
            new_id = max(post['id'] for post in posts) + 1
        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post_to_update = get_post_by_id(posts, post_id)

    if post_to_update is None:
        return "Post not found", 404

    if request.method == 'POST':
        post_to_update['title'] = request.form.get('title')
        post_to_update['author'] = request.form.get('author')
        post_to_update['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post_to_update)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)