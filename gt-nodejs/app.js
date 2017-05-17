require('./database');

var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session');
var app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.set('db-uri', "localhost:27017/globetrotter");
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
var sess = {secret: "globetrotter", resave: true, saveUninitialized: true}
app.use(session(sess));
app.use(express.static(path.join(__dirname, 'public')));

var homecontroller = require('./controllers/home');
app.use('/', homecontroller);

var usercontroller = require('./controllers/user');
app.use('/user', usercontroller);

var dialogcontroller = require('./controllers/dialog');
app.use('/dialog', dialogcontroller);

var searchcontroller = require('./controllers/search');
app.use('/search', searchcontroller);


// catch 404 and forward to error handler
app.use(function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

app.use(function (err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

var port = process.env.PORT || 8080;
var server = app.listen(port, function () {

});