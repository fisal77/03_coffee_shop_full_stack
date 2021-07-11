/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

// my login/signup Auth0 URL https://dev-4ktctw1t.us.auth0.com/authorize?audience=udacity-fsnd&response_type=token&client_id=WgsWTIxr13nPQP0eFFHcmkWOTmMZZUJh&redirect_uri=http://localhost:8100

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-4ktctw1t.us', // the auth0 domain prefix
    audience: 'udacity-fsnd', // the audience set for the auth0 app
    clientId: 'WgsWTIxr13nPQP0eFFHcmkWOTmMZZUJh', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
