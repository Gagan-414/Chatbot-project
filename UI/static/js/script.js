var senderId="user123"
// on input/text enter--------------------------------------------------------------------------------------
$('.usrInput').on('keyup keypress', function (e) {
    var keyCode = e.keyCode || e.which;
    var text = $(".usrInput").val();
    if (keyCode === 13) {
        if (text == "" || $.trim(text) == '') {
            e.preventDefault();
            return false;
        } else {
            $(".usrInput").blur();
            setUserResponse(text);
            send(text);
            e.preventDefault();
            return false;
        }
    }
});

//--------------------First Hello---------------------------
var id=123;
var j;
function firstHello(){
    var j=id;
    id=id+1;
    sessionStorage.setItem('j',j)
    let ele=document.getElementById('keypad')
    ele.value='Hello'
    var event = new KeyboardEvent('keypress',{key:'Enter',code:'Enter',keyCode:13,which:13});
    ele.dispatchEvent(event)
}

$(document).ready(()=>{
    senderId=Math.random().toString(36).substring(2,9)+"user"+Math.random().toString(36).substring(2,9)
    });

//-------------------------------------FOR POPUP MESSAGE -------------------------------------------

function createPopup(message) {
    let popup = document.createElement("div");
    popup.innerHTML = message;
    popup.style.position = "fixed";
    popup.style.bottom = "90px";
    popup.style.right = "20px";
    popup.style.backgroundColor = "#10709e";
    // popup.style.border = "1px solid #10709e";
    popup.style.borderRadius= "15px";
    popup.style.padding = "10px";
    popup.style.color = "white"
    popup.style.boxShadow = "0 4px 8px rgba(0,0,0,0.1)";

    document.body.appendChild(popup);

    setTimeout(() => { popup.remove(); }, 2000); // Remove popup after 6 seconds
}

window.onload = function() {
    // Automatically display the popup after the page loads
    createPopup("Welcome! How can I help you today?");
};


//------------------------------------- Set user response------------------------------------
function setUserResponse(val) {

    var UserResponse = '<img class="userAvatar" src=' + "./static/img/userAvatar.jpg" + '><p class="userMsg">' + val + ' </p><div class="clearfix"></div>';
    $(UserResponse).appendTo('.chats').show('slow');
    var sstorage = sessionStorage.getItem('chatbot')?sessionStorage.getItem('chatbot'):""
    sstorage += UserResponse;
    sessionStorage.setItem("chatbot",sstorage)
    $(".usrInput").val('');
    scrollToBottomOfResults();
    $('.suggestions').remove();
}

//---------------------------------- Scroll to the bottom of the chats-------------------------------
function scrollToBottomOfResults() {
    var terminalResultsDiv = document.getElementById('chats');
    terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}

function send(message) {
    $.ajax({
        url:  'https://bc95-49-36-183-75.ngrok-free.app/webhooks/rest/webhook',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "message": message,
            "sender": senderId
        }),
        success: function (data, textStatus) {
            if(data != null){
                    setBotResponse(data);
            }
        },
        error: function (errorMessage) {
            setBotResponse("");

        }
    });
}

//------------------------------------ Set bot response -------------------------------------
function setBotResponse(val) {
	setTimeout(function () {
        var BotResponse=""
		if (val.length < 1) {
			//if there is no response from Rasa
			msg = 'I couldn\'t get that. Let\' try something else!';

			BotResponse = '<img class="botAvatar" src="./static/img/botAvatar.png"><p class="botMsg">' + msg + '</p><div class="clearfix"></div>';
			$(BotResponse).appendTo('.chats').hide().fadeIn(1000);
            var sstorage = sessionStorage.getItem('chatbot')?sessionStorage.getItem('chatbot'):""
            sstorage += BotResponse;
            sessionStorage.setItem("chatbot",sstorage)
		} else {
			//if we get response from Rasa
			for (i = 0; i < val.length; i++) {
				//check if there is text message
				if (val[i].hasOwnProperty("text")) {
					BotResponse = '<img class="botAvatar" src="./static/img/botAvatar.png"><p class="botMsg">' + val[i].text + '</p><div class="clearfix"></div>';
					$(BotResponse).appendTo('.chats').hide().fadeIn(1000);
//					if(val[i].text='')
                    var sstorage = sessionStorage.getItem('chatbot')?sessionStorage.getItem('chatbot'):""
                    sstorage += BotResponse;
                    sessionStorage.setItem("chatbot",sstorage)
                    const a= val[i].text
                    array= a.split(' ')
                    if(array[0]==='Thank' && array[1]==='You')
                    {
                    $('#keypad').hide();
                    sessionStorage.clear()
                    }
				}

				//check if there is image
				if (val[i].hasOwnProperty("image")) {
					BotResponse = '<div class="singleCard">' +
						'<img class="imgcard" src="' + val[i].image + '">' +
						'</div><div class="clearfix">'
					$(BotResponse).appendTo('.chats').hide().fadeIn(1000);
                    var sstorage = sessionStorage.getItem('chatbot')?sessionStorage.getItem('chatbot'):""
                    sstorage += BotResponse;
                    sessionStorage.setItem("chatbot",sstorage)
				}

				//check if there is  button message
				if (val[i].hasOwnProperty("buttons")) {
					addSuggestion(val[i].buttons);
				}

			}
			scrollToBottomOfResults();
			document.getElementById('keypad').focus()
		}
       
	}, 500);
}


// ------------------------------------------ Toggle chatbot -----------------------------------------------
let i =1;
$('#profile_div').click(function () {
    $('.profile_div').toggle();
    $('.widget').toggle();
    var sstorage=sessionStorage.getItem('chatbot')
    if(sstorage){
        $(sstorage).appendTo('.chats').hide().fadeIn(1000)
    }
    else if(i)
    {
       
        firstHello();}
    scrollToBottomOfResults();

});

$('#close').click(function () {
    i=0;
    $('.profile_div').toggle();
    $('.widget').toggle();
});

// ------------------------------------------ Suggestions -----------------------------------------------

function addSuggestion(textToAdd) {
    setTimeout(function () {
        var suggestions = textToAdd;
        var suggLength = textToAdd.length;
        $(' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>').appendTo('.chats').hide().fadeIn(1000);
        // Loop through suggestions
        for (i = 0; i < suggLength; i++) {
            $('<div class="menuChips" data-payload=\''+(suggestions[i].payload)+'\'>' + suggestions[i].title + "</div>").appendTo(".menu");
        }
        scrollToBottomOfResults();
    }, 1000);
}

// on click of suggestions, get the value and send to rasa
$(document).on("click", ".menu .menuChips", function () {
    var text = this.innerText;
    var payload= this.getAttribute('data-payload');
    setUserResponse(text);
    send(payload);
    $('.suggestions').remove(); //delete the suggestions
});

//----------------------------------on load-----------------------
//---------------------------reload-----------------------------------
window.onload = function() {
    // Check if the page is reloaded (refreshed)
    console.log(performance.navigation.type)
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
        console.log("Page is reloaded");
        sessionStorage.clear(); // Clear session storage on refresh
    } else {
        console.log("Page is not reloaded (navigated or first visit)");
        // Session storage will be retained here
    }
};