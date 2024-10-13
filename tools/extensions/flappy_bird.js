
let bird;
let pipes = [];
let score = 0;

function setup() {
  createCanvas(400, 600);
  bird = new Bird();
  pipes.push(new Pipe());
}

function draw() {
  background(0);

  for (let i = pipes.length-1; i >= 0; i--) {
    pipes[i].show();
    pipes[i].update();

    if (pipes[i].hits(bird)) {
      console.log("HIT");
      noLoop();
    }

    if (pipes[i].offscreen()) {
      pipes.splice(i, 1);
      score++;
    }
  }

  bird.update();
  bird.show();

  if (frameCount % 75 == 0) {
    pipes.push(new Pipe());
  }

  fill(255);
  textSize(32);
  text("Score: " + score, 10, 30);
}

function mousePressed() {
  bird.up();
}

class Bird {
  constructor() {
    this.y = height / 2;
    this.x = 64;

    this.gravity = 0.6;
    this.lift = -15;
    this.velocity = 0;
  }

  show() {
    fill(255, 255, 0);
    ellipse(this.x, this.y, 32, 32);
  }

  up() {
    this.velocity += this.lift;
  }

  update() {
    this.velocity += this.gravity;
    this.y += this.velocity;

    if (this.y > height) {
      this.y = height;
      this.velocity = 0;
      noLoop();
    }

    if (this.y < 0) {
      this.y = 0;
      this.velocity = 0;
    }
  }
}

class Pipe {
  constructor() {
    this.spacing = 175;
    this.top = random(height / 6, 3 / 4 * height);
    this.bottom = height - (this.top + this.spacing);
    this.x = width;
    this.w = 20;
    this.speed = 6;
  }

  hits(bird) {
    if (bird.y < this.top || bird.y > height - this.bottom) {
      if (bird.x > this.x && bird.x < this.x + this.w) {
        return true;
      }
    }
    return false;
  }

  show() {
    fill(0, 255, 0);
    rect(this.x, 0, this.w, this.top);
    rect(this.x, height - this.bottom, this.w, this.bottom);
  }

  update() {
    this.x -= this.speed;
  }

  offscreen() {
    return this.x < -this.w;
  }
}
