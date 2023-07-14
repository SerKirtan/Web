document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function submit_email(event) {
  event.preventDefault()

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then( result => {
    if(result.error){
      alert(result.error);
      compose_email();
    } else{
      alert(result.message);
      load_mailbox('sent');
    }
  });
  // .then(response => load_mailbox('sent'));
}

function load_email(id) {
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    const div = document.querySelector('#email-view');
    div.innerHTML = `
        <div class="card-body>
          <h5 class="text-teal-700"><b>From: </b>${email['sender']}</h5>
          <h5 class="text-teal-700"><b>To: </b>${email['recipients']}</h5>
          <h5 class="text-gray-700"><b>Subject: </b> ${email['subject']} </h5>
          <small class="text-gray-700">${email['timestamp']} </small> 
          <hr>
            <p class="text-black-700">
              ${email['body']}
            </p>
          <hr>
        </div>
    `;

    // create reply

    const reply = document.createElement('button');
    reply.className="btn btn-primary";
    reply.innerHTML="Reply";
    reply.addEventListener('click' , () => {
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      document.querySelector('#compose-recipients').value =  email.sender;
      if(!email.subject.includes("Re: "))
        document.querySelector('#compose-subject').value = "Re: " + email.subject;
      else
        document.querySelector('#compose-subject').value = email.subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote ${email.body}`;
    });
    div.appendChild(reply);

    // create archive
    const archive = document.createElement('buuton');
    archive.style.marginLeft = '4px';
    archive.className  =  email.archived ? "btn btn-danger" :"btn btn-success";
    archive.innerHTML = email.archived ? "Unarchive" : "Archive";
    archive.addEventListener('click', () => {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ 
          archived : !email['archived']
        })
      })
      .then(response => load_mailbox('inbox'))
      
    });
    div.append(archive);
    
    readButton = document.createElement('button');
    readButton.className = "btn-secondary m-1";
    readButton.innerHTML = "Mark as Unread"
    readButton.addEventListener('click', function() {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ read : false })
      })
      .then(response => load_mailbox('inbox'))
    })
    div.appendChild(readButton);

    // mark this email as read
    if (!email['read']) {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ read : true })
      })
    }
  });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {

      emails.forEach(email => {
        let div = document.createElement('div');
        div.className = "card"
        div.style.marginBottom = '4px'
        div.style.backgroundColor = email['read'] ? '' : 'rgba(83, 79, 75, 0.3)';
        div.innerHTML = `
          <span class="sender col-4"> <b>${email['sender']}</b> </span>
          <span class="subject col-4" style="color: blueviolet"> Subject: ${email['subject']} </span>
          <small class="timestamp col-4"> ${email['timestamp']} </small>
        `;
        div.addEventListener('click', () => load_email(email['id']));
        document.querySelector('#emails-view').appendChild(div);

      });
    });
}