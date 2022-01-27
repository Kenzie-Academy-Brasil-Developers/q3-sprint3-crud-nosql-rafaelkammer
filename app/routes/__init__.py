from app.routes.posts import routes_posts

def init_app(app):
    routes_posts(app)