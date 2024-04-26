"use strict";
function setCookie(cookieName, cookieValue, expiryMins = 55) {
    let d = new Date();
    d.setTime(d.getTime() + (expiryMins * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";SameSite=Strict;path=/";
}
function getCookie(cookieName) {
    const code = cookieName + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(code) === 0) {
            return c.substring(code.length, c.length);
        }
    }
    return undefined;
}
function showAlert(alertText) {
    let successAlert = $('#success-alert');
    successAlert.text(alertText);
    successAlert.fadeIn();
    setTimeout(function () {
        successAlert.fadeOut();
    }, 10000); // 10 seconds in milliseconds
}
function wrongAnswer(alertText) {
    let warningAlert = $('#warning-alert');
    let entryBox = $('#attempt_text');
    let entryButton = $('#attempt_button');
    alertText = 'Not a valid codeword: "' + alertText + '". Try again in 20 seconds!';
    warningAlert.text(alertText);
    warningAlert.fadeIn();
    entryBox.attr('disabled', 'disabled');
    entryButton.attr('disabled', 'disabled');
    setTimeout(function () {
        warningAlert.fadeOut();
        entryBox.removeAttr('disabled');
        entryButton.removeAttr('disabled');
    }, 20000); // 20 seconds in milliseconds
}
const resetGame = 'PUZZLE_RESET_AZ89IQW3_';
const gameCookie = 'currentGame';
class Game {
    constructor(group) {
        this.groupLetter = '';
        this.puzzles = [];
        this.groupLetter = group.groupLetter;
        this.puzzles = group.puzzles;
    }
    static fromJSON(json) {
        return new Game({
            groupLetter: json.group_letter,
            puzzles: json.puzzles.map((puzzle) => {
                return {
                    name: puzzle.name,
                    codeword: puzzle.codeword,
                    solved: puzzle.solved ? new Date(puzzle.solved) : undefined
                };
            })
        });
    }
    toJSON() {
        return {
            groupLetter: this.groupLetter,
            puzzles: this.puzzles.map(puzzle => {
                return {
                    name: puzzle.name,
                    codeword: puzzle.codeword,
                    solved: puzzle.solved ? puzzle.solved.toISOString() : undefined
                };
            })
        };
    }
    getStats() {
        const total = this.puzzles.length;
        const solved = this.puzzles.filter(puzzle => puzzle.solved !== undefined).length;
        return {
            totalPuzzles: total,
            solvedPuzzles: solved
        };
    }
    saveGame() {
        // TODO: Implement saving game state
        const cookieName = 'game-' + this.groupLetter;
        setCookie(gameCookie, JSON.stringify(this.toJSON()), 60 * 24 * 7);
        setCookie(cookieName, JSON.stringify(this.toJSON()), 60 * 24 * 7);
    }
    attempt(attempt_word) {
        console.log('Attempted: ' + attempt_word);
        for (const puzzle of this.puzzles) {
            if (puzzle.codeword === attempt_word.toUpperCase()) {
                if (puzzle.solved === undefined) {
                    console.log('Solved: ' + puzzle.name);
                    showAlert('Solved: ' + puzzle.name);
                    puzzle.solved = new Date();
                    this.saveGame();
                }
                else {
                    console.log('Already solved: ' + puzzle.name);
                }
                return true;
            }
        }
        wrongAnswer(attempt_word);
        return false;
    }
}
// Set standard values for game time and cookie key
const gameTime = 1000 * 60 * 55;
const countDownKey = "countDownDate";
let game = new Game({ groupLetter: 'X', puzzles: [] });
let savedGame = getCookie(gameCookie);
if (savedGame !== undefined) {
    game = Game.fromJSON(JSON.parse(savedGame));
}
function newCountDownDate() {
    // Set time to 55 minutes from now.
    return new Date(new Date().getTime() + gameTime);
}
function setCountDownDate() {
    let returnDate = newCountDownDate();
    setCookie(countDownKey, returnDate.toISOString());
    return returnDate;
}
function getCountDownDate() {
    let target = getCookie(countDownKey);
    if (target === undefined) {
        return setCountDownDate();
    }
    let returnDate = new Date(target);
    if (returnDate.getTime() < new Date('2024-01-01').getTime()) {
        return setCountDownDate();
    }
    if (returnDate.getTime() < new Date().getTime()) {
        return setCountDownDate();
    }
    return returnDate;
}
function renderProgress(stats) {
    let progress = $('#progress');
    progress.text(stats.solvedPuzzles + ' / ' + stats.totalPuzzles);
}
// Update the count-down every 1 second
let x = setInterval(function () {
    // Get today's date and time
    let now = new Date().getTime();
    let countDownDate = getCountDownDate().getTime();
    // Find the distance between now and the countdown date
    let distance = countDownDate - now;
    let reset = (countDownDate + 1000 * 60 * 5) - now;
    // Time calculations for days, hours, minutes and seconds
    let days = Math.floor(distance / (1000 * 60 * 60 * 24));
    let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Display the result in the element with id="demo"
    // @ts-ignore
    document.getElementById("timer").innerHTML = minutes + "m " + seconds + "s ";
    renderProgress(game.getStats());
    // If the countdown is finished, write some text
    if (distance < 0) {
        clearInterval(x);
        // @ts-ignore
        document.getElementById("timer").innerHTML = "EXPIRED";
        if (reset < 0) {
            setCountDownDate();
        }
    }
}, 1000);
function makeGame(groupLetter) {
    $.ajax({
        type: 'GET',
        url: '/api/group/' + groupLetter,
        success: function (response) {
            game = Game.fromJSON(response);
            game.saveGame();
            console.log('Game Set: ' + game.groupLetter);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}
function fireAttempt(attemptText) {
    // Send an AJAX request to the API endpoint
    $.ajax({
        type: 'POST',
        url: '/api/attempt',
        data: { attempt_text: attemptText },
        success: function (response) {
            // Handle the API response here
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Handle any errors that occur during the API call
            console.error(error);
        }
    });
}
function makeAttempt(attemptText, form) {
    console.log('Attempt: ' + attemptText);
    form.trigger("reset");
    if (attemptText.includes(resetGame)) {
        console.log('Resetting game');
        let groupLetter = attemptText.replace(resetGame, '');
        makeGame(groupLetter);
        setCountDownDate();
        return;
    }
    if (game.attempt(attemptText)) {
        fireAttempt(attemptText);
    }
}
$(function () {
    const form = $('#attempt-form');
    // Attach an event listener to the form submission event
    form.on('submit', function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        // Serialize the form data into a query string
        const formData = $(this);
        const attemptText = formData.find('input[name="attempt_text"]').val();
        makeAttempt(attemptText, form);
    });
});
