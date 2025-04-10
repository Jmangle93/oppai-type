  <script>
import { CharacterTracker, CharacterStats } from '../tracker.js';
import { hiraganaRomajiPairs, katakanaRomajiPairs } from '../characterRomajiPairs.js';
export default {
name: 'Game',
data() {
    return {
    tracker: null,
    currentPrompt: null,
    promptStartTime: null,
    elapsedTime: '0.000',
    promptQueue: [],
    userInput: '',
    selectedCharacterGroups: ['kata_vowels', 'hira_vowels', 'hira_k', 'hira_t', 'hira_s'],
    };
},
created() {
    this.updatePromptQueue();
},
mounted() {
    this.initCanvas();
    this.drawPrompt();
    document.addEventListener('keyup', this.handleKeyPress);
    this.startTimer();
},
beforeDestroy() {
    document.removeEventListener('keyup', this.handleKeyPress); // Clean up
},
methods: {
    initCanvas() {
        const dpr = window.devicePixelRatio || 1;
        this.$refs.canvas.width = window.innerWidth * 0.5 * dpr;
        this.$refs.canvas.height = window.innerHeight * 0.4 * dpr;
        this.$refs.canvas.style.width = `${window.innerWidth * 0.5}px`;
        this.$refs.canvas.style.height = `${window.innerHeight * 0.4}px`;
    },
    updatePromptQueue() {
      const selectedPairs = this.selectedCharacterGroups.reduce((acc, key) => {
        if (katakanaRomajiPairs[key]) {
          acc[key] = katakanaRomajiPairs[key];
        }
        if (hiraganaRomajiPairs[key]) {
          acc[key] = hiraganaRomajiPairs[key];
        }
        return acc;
      }, {});
      this.promptQueue = Object.values(selectedPairs).flatMap(group => 
        Object.entries(group).map(([romaji, japanese]) => [romaji, japanese])
      );
      this.tracker = new CharacterTracker(this.promptQueue);
      this.currentPrompt = this.promptQueue[Math.floor(Math.random() * this.promptQueue.length)];
    },
    drawPrompt() {
      const ctx = this.$refs.canvas.getContext('2d');
      ctx.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
      ctx.font = '64px Arial';
      ctx.fillStyle = 'black';
      ctx.fillText(this.currentPrompt[1], this.$refs.canvas.width / 2 - 20, this.$refs.canvas.height / 2);
      this.promptStartTime = performance.now();
      this.updateTimer();
    },

    submitGuess() {
      const timeTaken = (performance.now() - this.promptStartTime) / 1000;
      const wasCorrect = this.userInput.toLowerCase() === this.currentPrompt[0].toLowerCase();
      this.tracker.updateStats(this.currentPrompt[0], this.currentPrompt[1], timeTaken, wasCorrect);
      this.userInput = ''; // Clear input
      if (wasCorrect) {
        this.promptStartTime = performance.now(); // Reset start time for next prompt
        this.currentPrompt = this.promptQueue[Math.floor(Math.random() * this.promptQueue.length)];
        this.drawPrompt();
      }
    },
    startTimer() {
      const update = () => {
        if (this.promptStartTime !== null) {
          const now = performance.now();
          this.elapsedTime = ((now - this.promptStartTime) / 1000).toFixed(3); // Update time in seconds with 3 decimal places
        }
        this.animationFrameId = requestAnimationFrame(update); // Schedule next update
      };
      this.animationFrameId = requestAnimationFrame(update); // Start the loop
    },
    updateTimer() {
      // Called when prompt changes to reset and update immediately
      this.elapsedTime = '0.000'; // Reset display
    }
  }
};
</script>

<template>
    <div id="game-container">
      <div class="game-area">
        <canvas id="canvas" ref="canvas"></canvas>
        <div class="timer">{{ elapsedTime }}s</div>
        <input v-model="userInput" @keyup.enter="submitGuess" placeholder="Type the romaji here..." class="user-input" />
      </div>
      <div id="stats-panel" ref="statsPanel" class="stats-panel">
        <h2>Statistics</h2>
        <div v-for="(stats, key) in tracker.stats" :key="key" class="stat-item">
          {{ key.split('|')[1] }} : Avg Speed: {{ stats.averageSpeed.toFixed(2) }}s, Attempts: {{ stats.attempts }}, Correct: {{ stats.successes }}
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