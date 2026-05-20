import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("""
   ╔══════════════════════════════════════════════════════╗
   ║                                                      ║
   ║      ██████╗ ███████╗██╗███╗   ██╗████████╗          ║
   ║     ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝          ║
   ║     ██║   ██║███████╗██║██╔██╗ ██║   ██║             ║
   ║     ██║   ██║╚════██║██║██║╚██╗██║   ██║             ║
   ║     ╚██████╔╝███████║██║██║ ╚████║   ██║             ║
   ║      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝             ║
   ║                                                      ║
   ║                    DEIGHTYG                          ║
   ║                                                      ║
   ║               USERNAME OSINT TOOL                    ║
   ║           Find accounts across 100+ sites            ║
   ╚══════════════════════════════════════════════════════╝
""")
# Get username
user = input('Enter the username: ').strip().lower()

# Define platforms to check
platforms = {
    # SOCIAL MEDIA (Major)
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://instagram.com/{}/",
    "Facebook": "https://facebook.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "LinkedIn": "https://linkedin.com/in/{}",
    "Pinterest": "https://pinterest.com/{}",
    "Snapchat": "https://snapchat.com/add/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Flickr": "https://flickr.com/people/{}",
    "Meetup": "https://meetup.com/members/{}",
    "Nextdoor": "https://nextdoor.com/profile/{}/",
    
    # VIDEO PLATFORMS
    "YouTube": "https://youtube.com/@{}",
    "Twitch": "https://twitch.tv/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Dailymotion": "https://dailymotion.com/{}",
    "Rumble": "https://rumble.com/user/{}",
    "Odysee": "https://odysee.com/@{}",
    "PeerTube": "https://peertube.tv/accounts/{}",
    
    # CODING & DEVELOPMENT
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}/",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "HackerRank": "https://hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}",
    "CodePen": "https://codepen.io/{}",
    "Replit": "https://replit.com/@{}",
    "CodeSandbox": "https://codesandbox.io/u/{}",
    "DevTo": "https://dev.to/{}",
    "Medium": "https://medium.com/@{}",
    "Hashnode": "https://hashnode.com/@{}",
    
    # FORUMS & COMMUNITIES
    "Quora": "https://quora.com/profile/{}",
    "StackExchange": "https://stackexchange.com/users/{}",
    "ProductHunt": "https://producthunt.com/@{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Lobsters": "https://lobste.rs/u/{}",
    "Scribd": "https://scribd.com/{}",
    "Slideshare": "https://slideshare.net/{}",
    "Behance": "https://behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "ArtStation": "https://artstation.com/{}",
    "DeviantArt": "https://deviantart.com/{}",
    
    # GAMING
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://xboxgamertag.com/search/{}",
    "PlayStation": "https://psnprofiles.com/{}",
    "Nintendo": "https://nintendo.com/users/{}",
    "EpicGames": "https://epicgames.com/id/{}",
    "BattleNet": "https://battlenet.com/{}",
    "Minecraft": "https://namemc.com/profile/{}",
    "Roblox": "https://roblox.com/user/profile/{}",
    "Discord": "https://discordlookup.com/user/{}",
    "Twitch": "https://twitch.tv/{}",
    "Kick": "https://kick.com/{}",
    "Rumble": "https://rumble.com/user/{}",
    
    # BLOGGING & WRITING
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Wix": "https://{}.wixsite.com",
    "Ghost": "https://{}.ghost.io",
    "Substack": "https://substack.com/@{}",
    "Tumblr": "https://{}.tumblr.com",
    
    # MUSIC & AUDIO
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "AppleMusic": "https://music.apple.com/profile/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Mixcloud": "https://mixcloud.com/{}",
    "Audiomack": "https://audiomack.com/{}",
    "LastFM": "https://last.fm/user/{}",
    
    # DATING (OSINT goldmine)
    "Tinder": "https://tinder.com/@{}",
    "Bumble": "https://bumble.com/profile/{}",
    "OkCupid": "https://okcupid.com/profile/{}",
    "PlentyOfFish": "https://pof.com/user/{}",
    "Hinge": "https://hinge.co/@{}",
    "Match": "https://match.com/profile/{}",
    "Grindr": "https://grindr.com/@{}",
    
    # PROFESSIONAL
    "AngelList": "https://angel.co/u/{}",
    "Crunchbase": "https://crunchbase.com/person/{}",
    "ResearchGate": "https://researchgate.net/profile/{}",
    "Academia": "https://academia.edu/{}",
    "GoogleScholar": "https://scholar.google.com/citations?user={}",
    "LinkedIn": "https://linkedin.com/in/{}",
    "Xing": "https://xing.com/profile/{}",
    
    # MESSAGING
    "Telegram": "https://t.me/{}",
    "Signal": "https://signal.me/#/{}",
    "WhatsApp": "https://wa.me/{}",  # Phone number, not username
    "Skype": "https://join.skype.com/invite/{}",
    
    # SHOPPING & REVIEWS
    "Amazon": "https://amazon.com/profile/{}",
    "Ebay": "https://ebay.com/usr/{}",
    "Etsy": "https://etsy.com/shop/{}",
    "Redbubble": "https://redbubble.com/people/{}",
    "Fiverr": "https://fiverr.com/{}",
    "Upwork": "https://upwork.com/freelancers/{}",
    "Freelancer": "https://freelancer.com/u/{}",
    
    # NEWS & CONTENT
    "Patreon": "https://patreon.com/{}",
    "BuyMeACoffee": "https://buymeacoffee.com/{}",
    "KoFi": "https://ko-fi.com/{}",
    "OnlyFans": "https://onlyfans.com/{}",
    "Linktree": "https://linktr.ee/{}",
    "BioSite": "https://bio.site/{}",
    "Carrd": "https://{}.carrd.co",
    
    # MISCELLANEOUS
    "Pastebin": "https://pastebin.com/u/{}",
    "GitHubGist": "https://gist.github.com/{}",
    "Keybase": "https://keybase.io/{}",
    "AboutMe": "https://about.me/{}",
    "Linktree": "https://linktr.ee/{}",
    "Linkkle": "https://linkkle.com/{}",
    "TapBio": "https://tap.bio/@{}",
    
    # COUNTRY SPECIFIC
    "VK": "https://vk.com/{}",
    "Line": "https://line.me/ti/p/@{}",
    "KakaoTalk": "https://story.kakao.com/{}",
}

def check_platform(name, url_pattern):
    """Check a single website for the username"""
    url = url_pattern.format(user)
    try:
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            return (name, url, True)  # Found
        else:
            return (name, url, False)  # Not found
    except:
        return (name, url, None)  # Error

print(f"\n🔍 Checking {len(platforms)} platforms for '{user}'...")

start_time = time.time()

# Store found profiles
found_profiles = []  # List of (platform_name, url)

# Check all sites at once
with ThreadPoolExecutor(max_workers=20) as executor:
    # Submit all tasks
    futures = {executor.submit(check_platform, name, pattern): name 
               for name, pattern in platforms.items()}
    
    # Process results as they come in
    completed = 0
    for future in as_completed(futures):
        completed += 1
        name, url, found = future.result()
        
        if found:
            print(f'✅ [{completed}/{len(platforms)}] {name}: FOUND')
            found_profiles.append((name, url))  # Save for later
        elif found is False:
            print(f'❌ [{completed}/{len(platforms)}] {name}: Not found')
        else:
            print(f'⚠️ [{completed}/{len(platforms)}] {name}: Error/timeout')

end_time = time.time()
total_time = end_time - start_time

# ============================================
# PRINT ALL FOUND LINKS AT THE END
# ============================================
print("\n" + "="*60)
print(f"📊 RESULTS FOR: {user}")
print("="*60)

if found_profiles:
    print(f"\n✅ FOUND {len(found_profiles)} PROFILE(S):\n")
    for i, (platform, url) in enumerate(found_profiles, 1):
        print(f"  {i}. {platform}: {url}")
else:
    print(f"\n❌ No profiles found for '{user}' on any platform")

print(f"\n⏱️  Time taken: {total_time:.2f} seconds")
print("="*60)