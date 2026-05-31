<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PopX Pro - Final Server Version</title>
  
  <!-- 🌐 ऑनलाईन क्लाऊड सर्व्हर जोडण्यासाठी Supabase लायब्ररी -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  
  <style>
    :root { --bg: #000; --text: #fff; --accent: #0095f6; --card: #121212; }
    body { background: var(--bg); color: var(--text); font-family: -apple-system, sans-serif; margin: 0; padding: 0; }
    
    /* 🔐 लॉगिन आणि साईनअप स्क्रीनचे कडक डिझाईन */
    .auth-container { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; padding: 25px; box-sizing: border-box; }
    .auth-box { width: 100%; max-width: 350px; text-align: center; }
    .auth-box input { width: 100%; padding: 14px; margin: 10px 0; background: #1c1c1e; border: 1px solid #333; border-radius: 8px; color: #fff; box-sizing: border-box; font-size: 15px; }
    
    /* 🚀 १००% टच वर्किंग बटणे */
    .btn-action { width: 100%; padding: 14px; background: var(--accent); border: none; color: white; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 15px; display: block; }
    .btn-switch { width: 100%; padding: 14px; background: #262626; border: 1px solid #444; color: #fff; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 20px; font-size: 15px; display: block; }
    
    /* 📱 मुख्य ॲप्लिकेशन लेआउट */
    .main-app { display: none; }
    .page { height: calc(100vh - 110px); overflow-y: auto; padding-bottom: 20px; box-sizing: border-box; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; border-bottom: 1px solid #262626; background: #000; height: 50px; box-sizing: border-box; }
    .logo { font-weight: bold; font-size: 24px; font-style: italic; background: linear-gradient(45deg, #f09433, #dc2743); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .bottom-nav { position: fixed; bottom: 0; width: 100%; background: #000; border-top: 1px solid #262626; display: flex; justify-content: space-around; padding: 12px 0; font-size: 24px; z-index: 1000; height: 60px; box-sizing: border-box; }
    .nav-btn { cursor: pointer; padding: 0 10px; }

    /* 📸 इंस्टाग्राम स्टाईल लेआउट्स */
    .stories-bar { display: flex; gap: 12px; padding: 10px; overflow-x: auto; border-bottom: 1px solid #1c1c1e; }
    .story-ring { width: 55px; height: 55px; border-radius: 50%; border: 2px solid #dc2743; padding: 2px; flex-shrink: 0; }
    .post-card { padding: 15px; border-bottom: 1px solid #1c1c1e; }
    .post-img { width: 100%; border-radius: 8px; margin-top: 10px; background: #111; min-height: 200px; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; margin-top: 10px; }
    .grid-item { aspect-ratio: 1/1; background-color: #222; background-size: cover; background-position: center; }
    .upload-box { width: 85%; border: 2px dashed #333; padding: 40px 10px; border-radius: 10px; margin: 0 auto 20px auto; cursor: pointer; background: #0a0a0a; }
    .btn-like { padding: 6px 12px; border: none; border-radius: 4px; background: var(--accent); color: white; cursor: pointer; font-weight: bold; margin-top: 8px; }
  </style>
</head>
<body>

  <!-- 🔐 १. LOGIN / SIGNUP SCREEN (इन्स्टाग्राम सारखी परफेक्ट डबल बटण सिस्टीम) -->
  <div id="auth-screen" class="auth-container">
    <div class="auth-box">
      <h1 class="logo" id="auth-logo-text" style="font-size: 42px; margin-bottom: 35px;">PopX Pro</h1>
      
      <div id="auth-form">
        <input type="email" id="auth-email" placeholder="Email Address">
        <input type="password" id="auth-password" placeholder="Password (Min 6 characters)">
        
        <!-- मुख्य निळे बटण -->
        <button id="auth-main-btn" class="btn-action" onclick="submitAuthentication()">Log In</button>
        
        <!-- खाते तयार करण्याचे ग्रे बटण -->
        <button id="auth-secondary-btn" class="btn-switch" onclick="toggleAuthViewMode()">Create New Account</button>
      </div>
    </div>
  </div>

  <!-- 📱 २. MAIN APP SCREEN (लॉगिन यशस्वी झाल्यावर ऑटोमॅटिक उघडणार) -->
  <div id="main-app-screen" class="main-app">
    <!-- Header -->
    <div class="header">
      <div class="logo">PopX Pro</div>
      <div style="font-size:14px; color:#ff4444; font-weight:bold; cursor:pointer; padding:5px;" onclick="handleUserLogout()">Logout 🚪</div>
    </div>

    <!-- 🏠 HOME PAGE (ऑनलाईन सर्व्हर लाईव्ह फीड) -->
    <div id="home-page" class="page" style="display: block;">
      <div class="stories-bar">
        <div class="story-ring"><div style="width:100%; height:100%; border-radius:50%; background:#333"></div></div>
        <div class="story-ring"><div style="width:100%; height:100%; border-radius:50%; background:#444"></div></div>
      </div>
      <div id="live-feed">
        <p style="text-align:center; color:#888; padding:30px;">Connecting to Cloud Server...</p>
      </div>
    </div>

    <!-- 🔍 SEARCH PAGE -->
    <div id="search-page" class="page" style="display: none;">
      <div style="padding:15px;"><input type="text" placeholder="Search accounts..." style="width:100%; padding:10px; border-radius:8px; border:none; background:#1c1c1e; color:#fff;"></div>
      <div class="grid" id="explore-grid"></div>
    </div>

    <!-- ➕ UPLOAD PAGE (गॅलरीवरून फोटो सर्व्हरवर पाठवणारी खणखणीत सिस्टीम) -->
    <div id="upload-page" class="page" style="display: none;">
      <div style="padding:40px; text-align:center;">
        <h3 style="margin-bottom:25px;">Create Live Post</h3>
        <div class="upload-box" onclick="document.getElementById('fileInput').click()">
          <span style="font-size:40px;">🖼️</span>
          <p id="uploadStatusText" style="margin:10px 0 0 0; color:#888;">Click to Open Gallery</p>
        </div>
        <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="imageSelected(this)">
        <input type="text" id="postCaption" placeholder="Write a caption..." style="width:85%; padding:12px; margin-bottom:25px; background:#1c1c1e; color:#fff; border:1px solid #333; border-radius:6px;"><br>
        <button onclick="uploadPostToCloudServer()" style="padding:12px 35px; background:#0095f6; border:none; color:white; border-radius:6px; font-weight:bold; cursor:pointer; width:85%;">Publish Post 🚀</button>
      </div>
    </div>

    <!-- 🎬 REELS PAGE -->
    <div id="reels-page" class="page" style="display: none;">
      <video style="width:100%; height:100%; object-fit:cover;" src="https://assets.mixkit.co/videos/preview/mixkit-girl-in-neon-sign-light-40492-large.mp4" loop autoplay muted></video>
    </div>

    <!-- 👤 PROFILE PAGE (तुमच्या सर्व जुन्या पोस्ट्स ऑनलाईन परत आणणारे पेज) -->
    <div id="profile-page" class="page" style="display: none;">
      <div style="padding:25px 20px; text-align:center;">
        <div style="width:85px; height:85px; border-radius:50%; background:#262626; margin:0 auto 10px auto; font-size:35px; display:flex; justify-content:center; align-items:center;">👤</div>
        <h3 id="profile-username" style="margin:5px 0;">Loading...</h3>
        <p style="color:#888; margin:5px 0 15px 0;">App Developer | Cloud Account Sync</p>
        <div class="grid" id="profile-grid"></div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
      <div class="nav-btn" onclick="openPage('home')">🏠</div>
      <div class="nav-btn" onclick="openPage('search')">🔍</div>
      <div class="nav-btn" onclick="openPage('upload')">➕</div>
      <div class="nav-btn" onclick="openPage('reels')">🎬</div>
      <div class="nav-btn" onclick="openPage('profile')">👤</div>
    </div>
  </div>

  <script>
    // 🔐 ऑनलाईन मोफत क्लाऊड सर्व्हरची लाईव्ह मास्टर चावी (Supabase Configuration)
    const SUPABASE_URL = "https://wzbxmscbttvpsomxqqwz.supabase.co";
    const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6Ynhtc2NidHR2cHNvbXhxcXd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwOTAwMDAsImV4cCI6MjAyNjg2MDAwMH0.1v7_AnOnL-mR_5UoW_uYvO7W3z7H5_Z6fO6h5_W7z7E";
    const supabase = Supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    let isLoginViewActive = true;
    let currentUserSession = null;
    let selectedImageFile = null;

    // युझर आधीपासून लॉग-इन आहे का ते तपासणे (Auto-Login System)
    async function checkExistingSession() {
      const { data } = await supabase.auth.getSession();
      if (data.session) {
        currentUserSession = data.session.user;
        displayMainApplication();
      }
    }
    checkExistingSession();

    // लॉगिन आणि साईनअप स्क्रीनमधील बटणे अदलाबदल करणे
    function toggleAuthViewMode() {
      isLoginViewActive = !isLoginViewActive;
      const mainBtn = document.getElementById('auth-main-btn');
      const secBtn = document.getElementById('auth-secondary-btn');
      const logoText = document.getElementById('auth-logo-text');

      if(isLoginViewActive) {
        logoText.innerText = "PopX Pro";
        mainBtn.innerText = "Log In";
        secBtn.innerText = "Create New Account";
        secBtn.style.background = "#262626";
        secBtn.style.color = "#fff";
      } else {
        logoText.innerText = "New Account 📝";
        mainBtn.innerText = "Register Account";
        secBtn.innerText = "Back to Log In";
        secBtn.style.background = "#331111";
        secBtn.style.color = "#ff4444";
      }
    }

    // 🔐 सर्व्हरवर लॉगिन आणि साईनअप सबमिट करणे
    async function submitAuthentication() {
      const email = document.getElementById('auth-email').value.trim();
      const password = document.getElementById('auth-password').value.trim();

      if (!email || !password) return alert("Please fill all details!");
      if (password.length < 6) return alert("Password must be at least 6 characters!");

      alert("Connecting to Cloud Server... Please wait!");

      if (isLoginViewActive) {
        // १. लॉग-इन करणे
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) return alert("Login Error: " + error.message);
        currentUserSession = data.user;
        alert("Welcome Back! 🚀");
        displayMainApplication();
      } else {
        // २. नवीन खाते तयार करणे
        const { data, error } = await supabase.auth.signUp({ email, password });
        if (error) return alert("Registration Error: " + error.message);
        alert("Account Created Successfully! You can Log In now. 🎉");
        isLoginViewActive = false;
        toggleAuthViewMode();
      }
    }

    function displayMainApplication() {
      document.getElementById('auth-screen').style.display = 'none';
      document.getElementById('main-app-screen').style.display = 'block';
      document.getElementById('profile-username').innerText = currentUserSession.email.split('@')[0] + " ✓";
      fetchCloudPosts();
    }

    function handleUserLogout() {
      supabase.auth.signOut();
      location.reload();
    }

    function openPage(id) {
      document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
      document.getElementById(id + '-page').style.display = 'block';
      if (id === 'home' || id === 'profile') fetchCloudPosts();
    }

    function imageSelected(input) {
      if(input.files && input.files[0]) {
        selectedImageFile = input.files[0];
        document.getElementById('uploadStatusText').innerText = "Selected: " + selectedImageFile.name;
        document.getElementById('uploadStatusText').style.color = "#0095f6";
      }
    }

    // 🚀 गॅलरी फोटो ऑनलाईन सर्व्हर स्टोरेजवर अपलोड करणे
    async function uploadPostToCloudServer() {
      const caption = document.getElementById('postCaption').value;
      if (!selectedImageFile) return alert("Please select an image first!");

      alert("Uploading Image to Cloud Storage... Please wait!");
      const fileName = Date.now() + "_" + selectedImageFile.name;
      
      // १. स्टोरेज बकेटमध्ये फोटो टाकणे
      const { data: storageData, error: storageError } = await supabase.storage
        .from('popx_photos')
        .upload('public/' + fileName, selectedImageFile);

      if (storageError) {
        console.error(storageError);
        return alert("Storage Error! Please choose a normal photo.");
      }

      // २. फोटोची ऑनलाईन लिंक मिळवणे
      const { data: urlData } = supabase.storage.from('popx_photos').getPublicUrl('public/' + fileName);
      const publicImageUrl = urlData.publicUrl;

      // ३. डेटाबेस टेबलमध्ये युझरनेमसह पोस्ट सेव्ह करणे
      const { error: dbError } = await supabase
        .from('popx_posts')
        .insert([{ 
          username: currentUserSession.email.split('@')[0], 
          image_url: publicImageUrl, 
          caption: caption || 'No caption' 
        }]);

      if (dbError) return alert("Database Save Error!");

      alert("Post Shared to Cloud Server! 🚀");
      
      // सर्व फॉर्म रीसेट करणे
      document.getElementById('fileInput').value = "";
      document.getElementById('postCaption').value = "";
      document.getElementById('uploadStatusText').innerText = "Click to Open Gallery";
      document.getElementById('uploadStatusText').style.color = "#888";
      selectedImageFile = null;
      
      openPage('home');
    }

    // 📥 सर्व्हरवरून डेटा सिंक करून लाईव्ह फीडवर दाखवणे
    async function fetchCloudPosts() {
      const feed = document.getElementById('live-feed');
      const profileGrid = document.getElementById('profile-grid');
      
      const { data: posts, error } = await supabase
        .from('popx_posts')
        .select('*')
        .order('id', { ascending: false });

      if (error) return;

      feed.innerHTML = "";
      if (profileGrid) profileGrid.innerHTML = "";

      if (!posts || posts.length === 0) {
        feed.innerHTML = '<p style="text-align:center; color:#888; padding:30px;">No posts on server yet. Upload your first pic!</p>';
        return;
      }

      posts.forEach(post => {
        // होम फीड कार्ड डिझाईन
        const card = document.createElement('div');
        card.className = 'post-card';
        card.innerHTML = `<b>@${post.username}</b> ✓<br><img class="post-img" src="${post.image_url}"><p>${post.caption}</p>
        <button class="btn-like" onclick="alert('Liked ❤️')">❤️ Like</button>`;
        feed.appendChild(card);

        // प्रोफाईल पेजवर जुन्या पोस्ट्स ऑटोमॅटिक सिंक होणार!
        if (currentUserSession && post.username === currentUserSession.email.split('@')[0]) {
          const item = document.createElement('div');
          item.className = 'grid-item';
          item.style.backgroundImage = `url(${post.image_url})`;
          if (profileGrid) profileGrid.appendChild(item);
        }
      });
    }

    // सर्च पेजसाठी एक्सप्लोर ग्रिड
    for(let i=0; i<6; i++) {
      const d = document.createElement('div'); d.className = 'grid-item';
      document.getElementById('explore-grid').appendChild(d);
    }
  </script>
</body>
</html>
