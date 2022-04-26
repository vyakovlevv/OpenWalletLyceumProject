from main import *

if __name__ == "__main__":
    db_session.global_init("db/database.db")
    app.register_blueprint(authorization.blueprint)
    app.register_blueprint(home.blueprint)
    api.add_resource(home_api.TokensListResource, '/api/tokens')
    api.add_resource(home_api.UserTokenListResource, '/api/users/tokens')
    api.add_resource(home_api.UserTokenResource, '/api/user/token')
    app.run(port=os.getenv('PORT', 8080), host='0.0.0.0')
