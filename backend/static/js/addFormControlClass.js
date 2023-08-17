    // add class 'form-control' to the inputs of a form context object passed from django view
    // the first element input is the csrf token, so start setting placeholders at element [1]
    let formFields = document.getElementsByTagName('input')
    formFields[1].placeholder = 'username'
    formFields[2].placeholder = 'email'
    formFields[3].placeholder = 'password'
    formFields[4].placeholder = 'confirm password'

    for (let field in formFields) {
        formFields[field].className += ' form-control'
    }