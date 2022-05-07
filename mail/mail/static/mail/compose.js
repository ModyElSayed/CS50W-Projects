function display_compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';
}

function compose_email() {

  // Show compose view and hide other views
  display_compose_email()

  // Clear out composition fields
  empty_fields();

}

function empty_fields() {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function predefined_fields(email) {
    document.querySelector('#compose-sender').value = email.sender;
    document.querySelector('#compose-recipients').value = email.recipients;
    document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.recipients +
                                                             ' wrote: ' + email.body;
    if (!email.subject.includes('Re: ')) {
        document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    } else {
        document.querySelector('#compose-subject').value = email.subject;
    }

}

function compose_reply(email) {
    display_compose_email();
    predefined_fields(email);
}

export { compose_email, compose_reply };