const config = {

  type: Phaser.AUTO,

  width: window.innerWidth,

  height: window.innerHeight,

  backgroundColor: 0x008800,

  scene: {

    preload: preload,

    create: create,

    update: update,

  },

};


const game = new Phaser.Game(config);


let bumblebee;

let jumpButton, leftButton, rightButton;

let jumpButtonDown = false;

let leftButtonDown = false;

let rightButtonDown = false;

let weightFactor = 1;

let gravityFactor = 1;

let verticalVelocity = 0;

let controllerBackground;

let background;


function preload() {

  // Load game assets here

}


function create() {

  background = this.add.tileSprite(0, 0, window.innerWidth, window.innerHeight, 0x000099).setOrigin(0, 0);

  bumblebee = this.add.rectangle(window.innerWidth / 2, window.innerHeight / 2, 50, 50, 0xffff00);


  // Add on-screen buttons

  controllerBackground = this.add.rectangle(window.innerWidth / 2, window.innerHeight - 40, window.innerWidth, 80, 0x008800);

  jumpButton = this.add.circle(100, window.innerHeight - 60, 20, 0x00ff00).setInteractive();

  leftButton = this.add.rectangle(window.innerWidth - 200, window.innerHeight - 60, 40, 40, 0xff0000).setInteractive();

  rightButton = this.add.rectangle(window.innerWidth - 100, window.innerHeight - 60, 40, 40, 0xff0000).setInteractive();


  jumpButton.on('pointerdown', () => (jumpButtonDown = true));

  jumpButton.on('pointerup', () => (jumpButtonDown = false));

  leftButton.on('pointerdown', () => (leftButtonDown = true));

  leftButton.on('pointerup', () => (leftButtonDown = false));

  rightButton.on('pointerdown', () => (rightButtonDown = true));

  rightButton.on('pointerup', () => (rightButtonDown = false));

}


function update() {

  if (leftButtonDown) {

    background.tilePositionX -= 5;

  } else if (rightButtonDown) {

    background.tilePositionX += 5;

  }


  if (jumpButtonDown) {

    verticalVelocity = Math.max(verticalVelocity - 2 / weightFactor, -10);

  } else {

    verticalVelocity = Math.min(verticalVelocity + 1 * gravityFactor, 5 * weightFactor);

  }


  bumblebee.y += verticalVelocity;


  if (bumblebee.y > window.innerHeight - 50 - bumblebee.height / 2) {

    bumblebee.y = window.innerHeight - 50 - bumblebee.height / 2;

    verticalVelocity = 0;

  } else if (bumblebee.y < 50 + bumblebee.height / 2) {

    bumblebee.y = 50 + bumblebee.height / 2;

  } else {

    verticalVelocity *= 0.95;

  }


  // Check for collision with left and right screen boundaries

  if (bumblebee.x < bumblebee.width / 2) {

    bumblebee.x = bumblebee.width / 2;

  } else if (bumblebee.x > window.innerWidth - bumblebee.width / 2) {

    bumblebee.x = window.innerWidth - bumblebee.width / 2;

  }


  // Check for collisions and update bee position

