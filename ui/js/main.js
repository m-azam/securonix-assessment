function onLogin() {
    var loginRequest = new XMLHttpRequest();
    var inputUsername = document.getElementById("username").value;
    var inputPassword = document.getElementById("password").value;
    loginRequest.withCredentials = true;

    loginRequest.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            var response = JSON.parse(this.responseText);
            if (response == inputUsername) {
                var sessionStorage = window.sessionStorage;
                sessionStorage.setItem('authUsername', inputUsername);
                sessionStorage.setItem('authPassword', inputPassword);
                window.location.href = "questions.html";
            } else {
                alert("Invalid username or password");
            }
        }
    });

    loginRequest.open("POST", "http://0.0.0.0:8000/login");
    loginRequest.setRequestHeader("Content-Type", "application/json");
    loginRequest.setRequestHeader("username", inputUsername);
    loginRequest.setRequestHeader("password", inputPassword);
    var data = JSON.stringify({ username: inputUsername, password: inputPassword });
    loginRequest.send(data);
}

function beginSurvey() {
    var questionRequest = new XMLHttpRequest();
    var sessionUsername = sessionStorage.getItem('authUsername');
    var sessionPassword = sessionStorage.getItem('authPassword');
    questionRequest.withCredentials = true;
    document.getElementById("beginSurvey").style.display = "none";
    document.getElementById("submiteSurvey").style.display = "block";

    questionRequest.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            var jsonData = JSON.parse(JSON.parse(this.response));
            var container = document.getElementById("questionContainer");
            window.sessionStorage.setItem('numberOfQuestions', jsonData.length);
            for (var index = 0; index < jsonData.length; index++) {
                var question = jsonData[index];
                container.innerHTML += '<div class="question-entry margin-bottom-big">'
                + '<h6>'+ question["questionCategory"] +'</h6>'
                + '<h7>'+ question["questionSub"] +'</h7>'
                + '<h3>'+ question["questionText"] +'</h3>'
                + '<select class="form-control margin" id="'+ question["questionId"] +'">'
                + '<option>0</option>'
                + ' <option>10</option>'
                + ' <option>15</option>'
                + ' <option>20</option>'
                + ' <option>25</option>'
                + ' <option>30</option>'
                + ' <option>35</option>'
                + ' <option>40</option>'
                + ' <option>45</option>'
                + ' <option>50</option>'
                + ' <option>55</option>'
                + ' <option>60</option>'
                + ' <option>65</option>'
                + ' <option>70</option>'
                + ' <option>75</option>'
                + ' <option>80</option>'
                + ' <option>85</option>'
                + ' <option>90</option>'
                + ' <option>95</option>'
                + ' <option>100</option>'
                + '</select>'
                + '</div>'
            }
        }
    });

    questionRequest.open("POST", "http://0.0.0.0:8000/questions");
    questionRequest.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({ username: sessionUsername, password: sessionPassword });
    questionRequest.send(data);
}

function surveySubmit() {
    var numberOfQuestions = window.sessionStorage.getItem('numberOfQuestions');
    var inputData = {};
    for (var index = 1; index <= numberOfQuestions; index++) {
        inputData[index.toString()] = document.getElementById(index).value;
    }
    var surveySubmissionRequest = new XMLHttpRequest();
    var sessionUsername = sessionStorage.getItem('authUsername');
    var sessionPassword = sessionStorage.getItem('authPassword');
    surveySubmissionRequest.withCredentials = true;

    surveySubmissionRequest.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {

        }
    });


    surveySubmissionRequest.open("POST", "http://0.0.0.0:8000/submit");
    surveySubmissionRequest.setRequestHeader("Content-Type", "application/json");
    surveySubmissionRequest.setRequestHeader("username", sessionUsername);
    surveySubmissionRequest.setRequestHeader("password", sessionPassword);
    var data = JSON.stringify(inputData);
    surveySubmissionRequest.send(data);
}