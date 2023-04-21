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
let score = 0;
let scoreText;

function preload() {
  // Load game assets here
}


  // Chat GTP Edit Part 2 Function Create Section

function create() {
  background = this.add.tileSprite(0, 0, window.innerWidth * 2, window.innerHeight, 0x000099).setOrigin(0, 0);
  bumblebee = this.add.rectangle(window.innerWidth / 2, window.innerHeight / 2, 50, 50, 0xffa500);
  bumblebee.setDepth(2); // Set the bumblebee's depth

  // Add the hive
  const hive = this.add.rectangle(50, window.innerHeight - 50, 100, 100, 0x996633);
  // Add flowers
  this.flowers = this.add.group();
  
  // Add pollen
  this.pollen = this.add.group();

  // Determine the number of flowers you want to create
  const numberOfFlowers = 10;

  for (let i = 0; i < numberOfFlowers; i++) {
    // Generate random x and y coordinates for the flowers
    let x, y;
    do {
      x = 100 + Math.random() * (window.innerWidth - 200);
      y = window.innerHeight - 200 - Math.random() * 100; // Adjust the y-coordinate range
    } while (this.flowers.getChildren().some(flower => {
      return Phaser.Geom.Intersects.CircleToCircle(
        new Phaser.Geom.Circle(x, y, 25),
        new Phaser.Geom.Circle(flower.x, flower.y, 25)
      );
    }));
    
    // Generate a random color for the flowers
    const colors = [0xff0000, 0x00ff00, 0x0000ff];
    const color = colors[Math.floor(Math.random() * colors.length)];

    // Add the flower at the generated coordinates with the random color
    addFlower.call(this, x, y, color);

    // Add the pollen at the generated coordinates
    addPollen.call(this, x, y - 10);
  }

  // Add collected pollen group
  this.collectedPollen = this.add.group();

 
  // Chat GTP Edit Part 3 Arcade Style Navigation Buttons

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

// Add this line to create the score text object
  scoreText = this.add.text(10, 10, `Score: ${score}`, { fontSize: '32px', color: '#ffffff' }).setDepth(5);
  
}



function addFlower(x, y, color) {
  const flower = this.add.circle(x, y, 25, color);
  flower.setDepth(1); // Set the flower's depth
  this.flowers.add(flower);
}


function addPollen(x, y) {
  const pollen = this.add.circle(x, y, 5, 0xffff00);
  pollen.setDepth(3); // Set the pollen's depth
  pollen.offset = { x: 0, y: 0 }; // Add offset property to store the initial offsets
  this.pollen.add(pollen);
}


  // Chat GTP Edit Part 4 Function Update


function update() {
  if (leftButtonDown) {
    scrollSpeed = 5;
  } else if (rightButtonDown) {
    scrollSpeed = -5;
  } else {
    scrollSpeed = 0;
  }

    // Add this line to call checkCollisions() function
  checkCollisions.call(this);



    // Update the position of the collected pollen using the stored offsets
  this.collectedPollen.getChildren().forEach((pollen) => {
    pollen.x = bumblebee.x + pollen.offset.x;
    pollen.y = bumblebee.y + pollen.offset.y;
  });

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


  function checkCollisions() {
    // Check for collisions with pollen
    this.pollen.getChildren().forEach((pollen) => {
      if (Phaser.Geom.Intersects.RectangleToRectangle(bumblebee.getBounds(), pollen.getBounds())) {
        this.pollen.remove(pollen); // Remove the pollen from the pollen group
        this.collectedPollen.add(pollen); // Add the pollen to the collectedPollen group
        pollen.offset.x = pollen.x - bumblebee.x; // Calculate and store the initial X-offset
        pollen.offset.y = pollen.y - bumblebee.y; // Calculate and store the initial Y-offset
        score += 5; // Increase the score
      }
    });

    // Update the score text object
    scoreText.setText(`Score: ${score}`);
  }
} // Move the closing brace here to fix the issue
