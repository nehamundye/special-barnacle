document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').onsubmit = send_email;
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show either inbox, sent, or archive mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails) // This returns an array of all emails
    

    // create a new element which will contain all email divs
    const div = document.createElement('div')
    div.className = "mail-list";
    // add the new element to DOM/div
    document.querySelector('#emails-view').append(div)



    emails.forEach(email => {
      console.log(email)
      console.log(`This is subject: ${email['subject']}`)
      console.log(`This is ID of the email: ${email['id']}`)
      console.log(`Read?: ${email['read']}`)

      // create a new element
      const div = document.createElement('div')
      // div.innerHTML =  `<a href="emails/${email['id']}"> <div>${email['sender']} | ${email['subject']}   |   ${email['timestamp']}</div></a>`
      div.innerHTML =  `<div>${email['sender']} | ${email['subject']}   |   ${email['timestamp']}</div>`

      // If the email is unread, it should appear with a white background. 
      // If the email has been read, it should appear with a gray background.
      if (email['read'] === false) {
        div.style.backgroundColor = 'white'
      } else {
        div.style.backgroundColor = 'grey'
      }
      // add the new element to DOM/div
      document.querySelector('.mail-list').append(div)
      
      // Listen: When any mail/partiuclar div is clicked, it should show details of that mail
      div.onclick = function() {
        // alert(email['id'])
        console.log(email['id'])
        load_mail(email['id'], mailbox)
        // When user clicks on a mail, then we dont need to show the inbox row 
        document.querySelector('.mail-list').remove()

      }
      
    })
    // document.querySelector('#emails-view > div > a > div').onclick = load_mail();
    
    
  })
}

// load individual mail details
function load_mail(email_id, mailbox) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email. This returns data in json format
    console.log(email);
    console.log(email.id)
    console.log(`MailBoxtype: ${mailbox}`)
    
    // create a new element
    const div = document.createElement('div')
    // show email’s sender, recipients, subject, timestamp, and body.
    div.innerHTML =  `<div>Sender: ${email['sender']}
        <br>
        Recipient: ${email['recipients']}
        <br>
        Subject: ${email['subject']}
        <br>
        Timestamp: ${email['timestamp']}
        <br>
        Body: ${email['body']}
      </div>`
    // add the new element to DOM/div
    document.querySelector('#emails-view').append(div)

    // if the mail opened is in inbox, show archive button. if archive button is clicked, archive the mail and load inbox
    // if the mail opened is in archive, show unarchive button. if unarchive button is clicked, unarchive the mail and load inbox

    if (mailbox === 'inbox') {
      console.log("entered mailbox")

      const replyArchiveButton = document.createElement('div')
      replyArchiveButton.innerHTML = `<button class="btn btn-primary" id="reply">Reply</button>
                                        <input id="archive" type="submit" value="Archive" class="btn btn-primary">`
      document.querySelector('#emails-view').append(replyArchiveButton)
      // const archiveButton = document.createElement('div')
      // const replyButton = document.createElement('div')
      // archiveButton.innerHTML =  `<input id="archive" type="submit" value="Archive" class="btn btn-primary">`
      // replyButton.innerHTML =  `<button class="btn btn-primary" id="reply">Reply</button>`
      // document.querySelector('#emails-view').append(archiveButton)
      // document.querySelector('#emails-view').append(replyButton)

      document.querySelector('#archive').onclick = function() {
        console.log(`give me email id: ${email.id}`)
        archive(email.id);
        console.log("Mail Archived");
        load_mailbox('inbox');
  
      }


      document.querySelector('#reply').addEventListener('click', function() {
        console.log('Reply button element has been clicked!')
        // When the user clicks the “Reply” button, they should be taken to the email composition form.
        compose_email()
        document.querySelector('#compose-recipients').value = email.sender
        if (email['subject'].startsWith("Re")) {
          document.querySelector('#compose-subject').value = `${email.subject}`
        } else {
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`
        }
        
        pre_fill = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n`;

        document.querySelector("#compose-body").value = pre_fill;

      })



    } else if (mailbox === 'archive') {
      const unarchiveButton = document.createElement('div')
      unarchiveButton.innerHTML =  `<input id="unarchive" type="submit" value="Unarchive" class="btn btn-primary">`
      document.querySelector('#emails-view').append(unarchiveButton)

      unarchiveButton.onclick = function() {
        console.log(`give me email id: ${email.id}`)
        unarchive(email.id);
        console.log("Mail Unarchived");
        load_mailbox('inbox');
  
      }
      
    }

  })
  .catch(error => {
    console.log('Error:', error);
  })

  // Once the email has been clicked on, you should mark the email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  
  
}

function send_email() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  console.log(`${recipients}, ${subject}, ${body}`)

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
    load_mailbox('sent')
  })
  .catch(error => {
    console.log('Error:', error);
  })


  return false;
}

function archive(email_id) {
    // Once the archived has been clicked on, you should mark the email as archived
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
}

function unarchive(email_id) {
  // Once the archived has been clicked on, you should mark the email as archived
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
}
