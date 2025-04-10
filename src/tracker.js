class CharacterTracker {
    constructor(promptQueue) {
      this.stats = {};
      promptQueue.forEach(([romaji, japanese]) => {
        this.stats[[romaji, japanese].join('|')] = new CharacterStats();
      });
    }
  
    updateStats(romaji, japanese, timeTaken, wasCorrect) {
        const key = [romaji, japanese].join('|');
        if (!this.stats[key]) {
            this.stats[key] = new CharacterStats();
        }
        this.stats[key].update(timeTaken, wasCorrect);
    }
  
    getStats(romaji, japanese) {
      return this.stats[[romaji, japanese].join('|')] || new CharacterStats();
    }
}
  
class CharacterStats {
    constructor() {
        this.attempts = 0;
        this.totalTime = 0;
        this.successes = 0;
        this.individualTimes = [];
    }

    update(timeTaken, wasCorrect) {
        this.attempts++;
        this.totalTime += timeTaken;
        this.individualTimes.push(timeTaken);
        if (wasCorrect) this.successes++;
    }

    get averageSpeed() { return this.attempts ? this.totalTime / this.attempts : 0; }
    get accuracy() { return this.attempts ? (this.successes / this.attempts) * 100 : 0; }
    get consistency() { 
        if (this.individualTimes.length < 2) return 1;
        const mean = this.individualTimes.reduce((a, b) => a + b) / this.individualTimes.length;
        const variance = this.individualTimes.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / this.individualTimes.length;
        return 1 / (variance + 1);
    }
}

export { CharacterTracker, CharacterStats };