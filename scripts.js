let interval = null;

const setButtonLoading = () => {
    document.getElementById("generate").innerHTML = `
        <div>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Loading...
        </div>
    `;
}

const setButtonFinished = () => {
    document.getElementById("generate").innerHTML = 'Generate';
}

const setImage = (src) => {
    document.getElementById("image").src = src;
}


(function(){
    clearInterval(interval);

    document.getElementById("generate").addEventListener("click", () => {
        setButtonLoading();
        fetch('https://2gotexgdyd.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseInit')
        .then(res => 
            res.json().then(body => {
                console.log(body)
                interval = setInterval(() => {
                    fetch("https://mcvwsqrip4.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseStatus", {
                        method: "POST",
                        body: JSON.stringify({
                            arn: body.executionArn
                        })
                      })
                    .then(res => 
                        res.json().then(body => {
                            console.log(body)
                            if (body['status'] === 'SUCCEEDED') {
                                clearInterval(interval);
                                setButtonFinished();
                                src = JSON.parse(body['output'])['body']['output'];
                                setImage(src.replaceAll('+', '%2B'));
                            }
                        })
                    )
                }, 3000)
            })
        )
    });
})();