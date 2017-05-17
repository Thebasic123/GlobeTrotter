var mongoose = require('mongoose');
var crypto = require('crypto');
var express = require('express');
var router = express.Router();
var User = mongoose.model('user');


router.post('/login', function (req, res) {
	var hash = crypto.createHash('md5').update(req.body.pass).digest('hex');
	User.findOne({
		email: req.body.email, 
		password: hash
	}, function (err, user){
		if (err) {
			req.send(err);
		}
		else if (user){
			req.session.user = req.body.email;
			req.session._id = user._id;
			delete req.session.error;
			res.redirect(req.protocol + "://" + req.get('host'));
		}
		else {
			req.session.error = "Wrong email or password";
			res.redirect(req.protocol + "://" + req.get('host') + "/dialog/login");
		}
	});
});

router.post('/logout', function (req, res){
	if (req.session.user) {
		delete req.session.user;
		delete req.session._id;
	}
	res.redirect(req.protocol + "://" + req.get('host'));
});

router.post('/register', function (req, res) {
	if (req.body.pass < 6) {
		req.session.error = "Your password is too short, it must be at least 6 characters";
		res.redirect(req.protocol + "://" + req.get('host') + "/dialog/register");
	}
	else if (req.body.pass == req.body.passconfirm) {
		var hash = crypto.createHash('md5').update(req.body.pass).digest('hex');
		new User({
			email: req.body.email, 
			password: hash
		}).save(function (err, user) {
			if (err) {
				if (11000 === err.code || 11001 === err.code) {
					req.session.error = "This email has already been registered on this site";
					res.redirect(req.protocol + "://" + req.get('host') + "/dialog/register");
				} else {
					res.send(err);
				}
			} else {	
				req.session.user = req.body.email;
				req.session._id = user._id;
				res.redirect(req.protocol + "://" + req.get('host'));
			}
		});	
	} else {
		req.session.error = "You must confirm your password";
		res.redirect(req.protocol + "://" + req.get('host') + "/dialog/register");
	}
});

module.exports = router;