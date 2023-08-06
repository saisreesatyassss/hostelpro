// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAO-Hy4wkxklCe7_ukRCnpsrtp3_ydQ658",
  authDomain: "hackthonipl.firebaseapp.com",
  projectId: "hackthonipl",
  storageBucket: "hackthonipl.appspot.com",
  messagingSenderId: "84414778347",
  appId: "1:84414778347:web:a9dc750ae262ed57f6a7ae",
  measurementId: "G-EWRV7FW2CB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);