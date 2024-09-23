

class BoggleGame {
    constructor(boardID, secs = 60) {
        console.log("Game Started");
        this.secs = secs; 
        this.showTimer(); 

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardID);
        this.timer = setInterval(this.tick.bind(this), 1000);
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

  
    async tick() {
        console.log(`Tick called. Seconds left: ${this.secs}`);
        this.secs -= 1;
        this.showTimer();
        if(this.secs === 0) {
            clearInterval(this.timer);
            await this.finalScore();
        }
    }
    showTimer() {
        console.log(`Timer updated: ${this.secs}`);
        console.log(this);
        const timerElement = $(".timer", this.board);
        timerElement.text(this.secs);
    }

    async finalScore() {
        $(".add-word", this.board).hide();
        const response = await axios.post("/post-score", {score: this.score});

        if (response.data.brokeRecord) {
            this.showMessages(`New High Score : ${this.score}`, "ok");
        }
        else  {
            this.showMessages(`Final Score: ${this.score}`, "ok");
        }
    }

    showWord(word) {
        $(".words", this.board).append($("<li>", {text: word}));
    }

    showScore() {
        $(".score", this.board).text(this.score);
    }

    showMessages(msg, cls){
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }


    async handleSubmit(evt) {
        
        evt.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val().toLowerCase();
        if (!word) return;

        if(this.words.has(word)) {
            this.showMessages(`Word: ${word} has already been found`, "error");
            return;
        }
        try {
            const responce = await axios.get("/check-word", {params: {word:word}});
            if (responce.data.result === "not-word") {
                this.showMessages(`${word} is not a valid English word`, "error");
            }
            else if (responce.data.result === "not-on-board") {
                this.showMessages(`${word} is not on the board`, "error");
            }
            else {
                this.showWord(word);
                this.score += word.length;
                this.showScore();
                this.words.add(word);
                this.showMessages(`Added: ${word}`, "good");
            }
        }
        catch (error) {
            console.log("error checking word:", error);
        }
        $word.val("").focus();
    }
}

