let score = 0;

$("#guess-form").on("submit", (e) => {
  // Prevent form from submitting
  e.preventDefault();
  // Grab form input value
  const $formValue = $("#guess").val();

  //   Axios request
  axios({
    method: "post",
    url: "/",
    data: {
      guess: $formValue,
    },
  })
    .then((response) => {
      generate_word(response.data);
      generate_score(response.data, $formValue);
    })
    .catch((error) => {
      console.log(error);
    });
});

const generate_word = (res) => {
  $(".guessed").html(`<p>The word you typed is: ${res.result}</p>`);
};

const generate_score = (res, word) => {
  if (res.result === "ok") {
    score += word.length;
    $(".score").html(`<p>Score:${score}</p>`);
  }
  let counter = 60;
  if ($(".counter").is(":empty")) {
    const counter_setup = setInterval(() => {
      $(".counter").html(counter--);
      if (counter == 1) {
        $(".counter").hide();
        $("#guess-form").hide().unbind("submit").submit();
        clearInterval(counter_setup);
      }
    }, 1000);
  }
  send_score(score);
};

const send_score = (score) => {
  axios({
    method: "post",
    url: "/completed",
    data: {
      score,
    },
  })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
};
