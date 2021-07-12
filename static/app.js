// Data variables
class BoggleGame {
    constructor(boardId, secs = 60) {
        this.secs = secs;
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $('#' + boardId);
        this.timer = setInterval(this.countDown.bind(this), 1000);

        $('.word-input', this.board).on('submit', this.handleSubmit.bind(this));
    }

    showWord(word) {
        $('.words', this.board).append($('<li>', {text: word}));
    }

    showScore() {
        $('.score', this.board).text(this.score);
    }

    showMessage(msg, type) {
        $('.msg')
            .text(msg)
            .removeClass()
            .addClass(`msg ${type}`);
    }

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $('.word', this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, 'err');
            return;
        }
    
        const res = await axios.get('/check', {params: {word: word}});
        if (res.data.result === 'not-word') {
            this.showMessage(`${word}'s not a word!`, "err");
        } else if (res.data.result === 'not-on-board') {
            this.showMessage(`${word}'s not on the board!`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`${word} added!`, "ok");
        }

        $word.val('').focus();
    }

    showTimer() {
        $('.timer', this.board).text(this.secs);
    }

    async countDown() {
        this.secs--;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $('.word-input', this.board).hide();
        const res = await axios.post('/post-score', {score: this.score});
        if (res.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, 'ok');
        } else {
            this.showMessage(`Final score: ${this.score}`, 'ok');
        }
    }
}
