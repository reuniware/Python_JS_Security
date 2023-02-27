// from https://stackoverflow.com/questions/64863099/deleting-tweets-with-js-console    

(async () => {
      function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    
      let found;
    
      while (found = document.querySelectorAll('[data-testid="caret"]').length) {
    
        // get first tweet
        let tweet = document.querySelectorAll('[data-testid="tweet"]')[0];
    
        // if it is a retweet, undo it
        if (tweet.querySelectorAll('[data-testid="unretweet"]').length) {
          tweet.querySelectorAll('[data-testid="unretweet"]')[0].click()
          await sleep(1000)
          document.querySelectorAll('[data-testid="unretweetConfirm"]')[0].click()
          await sleep(1000)      
        }
        // is a tweet
        else {
          if (new Date(document.querySelectorAll('[datetime]')[0].getAttribute('datetime')) < new Date('2018')) {
            console.log('Limit date reach')
            break;
          }
    
          tweet.querySelectorAll('[data-testid="caret"]')[0].click()
          await sleep(1000)
          document.querySelectorAll('[role="menuitem"]')[0].click()
          await sleep(1000)
          document.querySelectorAll('[data-testid="confirmationSheetConfirm"]')[0].click()
        }
      }
    
      if (!found)
        console.log('No more tweets found');
    
    })();
