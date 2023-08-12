## StockBot for Discord

**StockBot** is a Discord bot designed to allow users to virtually trade and manage stocks directly from their Discord application. It integrates with Firebase for database storage and leverages the `yfinance` module for real-time stock details.

### Features:

- **Real-time Stock Details**: Fetch and display up-to-date information about stocks.
- **Virtual Trading**: Engage in buying and selling of virtual stocks.
- **Profile Management**: Personalized user profiles for tracking balance and stock portfolio.
- **Net Worth**: A quick glance at your portfolio's total worth, factoring in both cash and stocks.

### 🚀 Getting Started

#### Prerequisites:

1. Ensure you have Python installed.
2. Setup a Firebase project with a real-time database.
3. Have your Discord bot token handy.
4. Install the required Python libraries: `discord.py`, `firebase_admin`, `yfinance`, and `python-dotenv`.

#### Setup:

1. **Firebase**:
   - Create your Firebase project and initiate a real-time database.
   - Obtain your Firebase service account key (`.json` format) and save it in your directory.
  
2. **Discord Bot**:
   - Navigate to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Generate a bot within your application and copy the bot TOKEN.
   
3. **Environment Setup**:
   - Populate your `.env` file with:
     ```
     DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
     ```

4. **Run the Bot**:
   - Run the provided Python script.
   - Send an invitation to your bot to join your Discord server.

### 📜 Commands:

- **$create**: Kickstarts a new profile with a default balance of $100,000.
- **$buy <stock code> <amount>**: Purchase a stock in the mentioned amount at its current price.
- **$sell <stock code> <amount>**: Offload a stock in the specified quantity at its current price.
- **$profile**: View your stock holdings and cash balance.
- **$money**: Check your prevailing balance.
- **$info <stock code>**: Dive deep into a specific stock's details.
- **$help**: A guide to all the commands at your disposal.
