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
  background = this.add.tileSprite(0, 0, window.innerWidth * 2, window.innerHeight, 0x000099).setOrigin(0, 0);
  bumblebee = this.add.rectangle(window.innerWidth / 2, window.innerHeight / 2, 50, 50, 0xffa500);
  bumblebee.setDepth(2); // Set the bumblebee's depth

  // Add the hive
  const hive = this.add.rectangle(50, window.innerHeight - 50, 100, 100, 0x996633);

  // Add flowers
  this.flowers = this.add.group();
  addFlower.call(this, 100, window.innerHeight - 150, 0xff0000);
  addFlower.call(this, 200, window.innerHeight - 200, 0x00ff00);
  addFlower.call(this, 300, window.innerHeight - 170, 0x0000ff);

  // Add pollen
  this.pollen = this.add.group();
  addPollen.call(this, 100, window.innerHeight - 160);
  addPollen.call(this, 200, window.innerHeight - 210);
  addPollen.call(this, 300, window.innerHeight - 180);


  

  // Add on-screen buttons
  controllerBackground = this.add.rectangle(window.innerWidth / 2, window.innerHeight - 50, window.innerWidth, 100, 0x008800);
  controllerBackground.setDepth(3); // Set the controller background's depth

  jumpButton = this.add.circle(100, window.innerHeight - 50, 25, 0x00ff00).setInteractive();
  jumpButton.setDepth(4); // Set the jump button's depth

  leftButton = this.add.triangle(window.innerWidth - 200, window.innerHeight - 50, 0, 25, 50, 0, 25, 50, 0xff0000).setInteractive();
  leftButton.setDepth(4); // Set the left button's depth

  rightButton = this.add.triangle(window.innerWidth - 100, window.innerHeight - 50, 50, 25, 0, 0, 25, 50, 0xff0000).setInteractive();
  rightButton.setDepth(4); // Set the right button's depth

  jumpButton.on('pointerdown', () => (jumpButtonDown = true));
  jumpButton.on('pointerup', () => (jumpButtonDown = false));
  leftButton.on('pointerdown', () => (leftButtonDown = true));
  leftButton.on('pointerup', () => (leftButtonDown = false));
  rightButton.on('pointerdown', () => (rightButtonDown = true));
  rightButton.on('pointerup', () => (rightButtonDown = false));

  // Create a camera that follows the bumblebee
  this.cameras.main.startFollow(bumblebee, true, 0.05, 0.05);
  this.cameras.main.setBounds(0, 0, window.innerWidth, window.innerHeight);
}

function addFlower(x, y, color) {
  const flower = this.add.circle(x, y, 25, color);
  flower.setDepth(1); // Set the flower's depth
  this.flowers.add(flower);
}

function addPollen(x, y) {
  const pollen = this.add.circle(x, y, 5, 0xffff00);
  pollen.setDepth(3); // Set the pollen's depth
  this.pollen.add(pollen);
}

function update() {
  if (leftButtonDown) {
    scrollSpeed = 5;
  } else if (rightButtonDown) {
    scrollSpeed = -5;
  } else {
    scrollSpeed = 0;
  }

  // Move the background
  background.tilePositionX += scrollSpeed;

  // Move the pollen and flowers in the opposite direction
  this.pollen.getChildren().forEach((pollen) => {
    pollen.x -= scrollSpeed;
  });

  this.flowers.getChildren().forEach((flower) => {
    flower.x -= scrollSpeed;
  });

  if (jumpButtonDown) {
    verticalVelocity = Math.max(verticalVelocity - 2 / weightFactor, -10);
  } else {
    verticalVelocity = Math.min(verticalVelocity + 1 * gravityFactor, 5 * weightFactor);
  }

  bumblebee.y += verticalVelocity;

  if (bumblebee.y > window.innerHeight - 50 - 75) { // Add -100 to the height
    bumblebee.y = window.innerHeight - 50 - 75;
    verticalVelocity = 0;
  } else if (bumblebee.y < 50) {
    bumblebee.y = 50;
    verticalVelocity = 1;
  }
}



function addFlower(x, y, color) {
  const flower = this.add.circle(x, y, 25, color);
  this.flowers.add(flower);
}

function addPollen(x, y) {
  const pollen = this.add.circle(x, y, 5, 0xffff00);
  this.pollen.add(pollen);
}
