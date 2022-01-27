from app.controllers import post_controller

def routes_posts(app):
    @app.get("/posts")
    def read_posts():
        return post_controller.retrieve_all()

    @app.get("/posts/<id>")
    def read_post_by_id(id):
        return post_controller.retrieve_one(id)

    @app.post("/posts")
    def create_post():
        return post_controller.create_post()

    @app.delete("/posts/<id>")
    def delete_post(id):
        return post_controller.delete_post(id)

    @app.patch("/posts/<id>")
    def update_post(id):
        return post_controller.update_post(id)