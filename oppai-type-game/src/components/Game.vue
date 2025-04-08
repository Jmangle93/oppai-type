  <script>
import { CharacterTracker, CharacterStats } from './tracker.js';
export default {
name: 'Game',
data() {
    return {
    tracker: new CharacterTracker([]),
    currentPrompt: ['ka', 'か'],
    lastTimestamp: performance.now(),
    promptQueue: [['ka', 'か'], ['sa', 'さ']],
    userInput: '',
    };
},
mounted() {
    console.log('Tracker initialized:', this.tracker);
    this.drawPrompt();
    document.addEventListener('keyup', this.handleKeyPress);
},
beforeDestroy() {
    document.removeEventListener('keyup', this.handleKeyPress); // Clean up
},
methods: {
    drawPrompt() {
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
      ctx.font = '48px Arial';
      ctx.fillStyle = 'black';
      ctx.fillText(this.currentPrompt[1], this.$refs.canvas.width / 2 - 20, this.$refs.canvas.height / 2);
      ctx.font = '24px Arial';
      ctx.fillText(`Type: ${this.currentPrompt[0]}`, this.$refs.canvas.width / 2 - 50, this.$refs.canvas.height / 2 + 50);
    },
    handleKeyPress(event) {
      if (event.key === 'Enter') {
        this.submitGuess();
      }
    },
    submitGuess() {
      const timeTaken = (performance.now() - this.lastTimestamp) / 1000;
      const wasCorrect = this.userInput.toLowerCase() === this.currentPrompt[0].toLowerCase();
      this.tracker.updateStats(this.currentPrompt[0], this.currentPrompt[1], timeTaken, wasCorrect);
      this.userInput = ''; // Clear input
      if (wasCorrect) {
        this.lastTimestamp = performance.now(); // Reset start time for next prompt
        console.log(this.tracker.getStats());
      }
      this.currentPrompt = this.promptQueue[Math.floor(Math.random() * this.promptQueue.length)];
      this.drawPrompt();
    }
  }
};
</script>

<template>
    <div id="game-container">
      <div class="game-area">
        <canvas id="canvas" ref="canvas"></canvas>
        <input v-model="userInput" @keyup.enter="submitGuess" placeholder="Type the romaji here..." class="user-input" />
      </div>
      <div id="stats-panel" ref="statsPanel" class="stats-panel">
        <h2>Statistics</h2>
        <div v-for="(stats, key) in tracker.stats" :key="key" class="stat-item">
          {{ key.split('|')[0] }} ({{ key.split('|')[1] }}): Avg Speed: {{ stats.averageSpeed.toFixed(2) }}s, Accuracy: {{ stats.accuracy.toFixed(1) }}%, Consistency: {{ stats.consistency.toFixed(2) }}
        </div>
      </div>
    </div>
</template>
  
<style scoped>
#game-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background: #f0f0f0; /* Light background for contrast */
  padding: 20px;
  box-sizing: border-box;
}

.game-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  margin-bottom: 20px;
}

#canvas {
  max-width: 100%;
  max-height: 100%;
  border: 1px solid #ccc; /* Optional: Add border for visibility */
}

.user-input {
  margin-top: 20px;
  padding: 10px;
  font-size: 18px;
  width: 300px; /* Fixed width for consistency */
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-panel {
  width: 90%; /* Take up most of the width */
  max-width: 1200px; /* Cap at a reasonable max width */
  background: #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* Enable scrolling if content overflows */
  max-height: 40vh; /* Limit height to 40% of viewport height */
}

h2 {
  margin-top: 0;
  color: #333;
  font-size: 24px;
}

.stat-item {
  margin-bottom: 15px;
  font-size: 16px;
  color: #444;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .stats-panel {
    width: 95%; /* Full width on mobile */
    max-height: 30vh; /* Smaller on mobile */
  }

  .user-input {
    width: 80%; /* Adjust input width on mobile */
  }

  #canvas {
    width: 80%; /* Smaller canvas on mobile */
    height: auto; /* Maintain aspect ratio */
  }
}
</style>