var mongoose = require('mongoose');
var express = require('express');
var router = express.Router();

router.get('/login', function (req, res){
	if (!req.session.user) {
		var error;
		if (req.session.error) {
			error = req.session.error;
			delete req.session.error;
		}
		res.render('dialog_login', {logo: "GlobeTrotter", error: error});
	} else {
		res.redirect(req.protocol + "://" + req.get('host'));
	}
});

router.get('/register', function (req, res){ 
	if (!req.session.user) {
		var error;
		if (req.session.error) {
			error = req.session.error;
			delete req.session.error;
		}
		res.render('dialog_register', {logo: "GlobeTrotter", error: error});
	} else {
		res.redirect(req.protocol + "://" + req.get('host'));
	}
});

module.exports = router;