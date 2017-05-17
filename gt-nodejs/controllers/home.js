var express = require('express');
var router = express.Router();

router.get('/', function (req, res){
	var authorised = (req.session.user)? true: false;
	res.render('index', {title: 'GlobeTrotter', authorised: authorised});
});

module.exports = router;