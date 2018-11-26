var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
router.get('/project1', function(req, res, next) {
  res.render('project1.ejs', { title: 'Project1' });
});
router.get('/paper_review', function(req, res, next) {
  res.render('paper_review.ejs', { title: 'paper review' });
});
router.get('/final_project', function(req, res, next) {
  res.render('final_project.ejs', { title: 'FINAL PROJECT' });
});

module.exports = router;
