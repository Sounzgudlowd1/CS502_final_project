var express = require('express');
var ps = require('python-shell');

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
router.get('/dfs_app', function(req, res, next) {
  var data_uploaded = 'false';
  res.render('dfs_app.ejs', { data_uploaded:  data_uploaded, title: 'DFS APP' });
});
//file handler
router.post('/upload', function(req, res) {
  console.log(req.files.filedata); // the uploaded file object

  var filedata = req.files.filedata;

  filedata.mv('uploads/datafile.txt', function(err) {
  if (err)
    return res.status(500).send(err);
  });
  var data_uploaded = 'true';
  res.render('dfs_app.ejs', { data_uploaded: data_uploaded  });

  ps.PythonShell.run('template_code/feedforward_nn.py', null, function (err, res) {
    if (err) throw err;
    console.log(res);
  });

});


module.exports = router;
