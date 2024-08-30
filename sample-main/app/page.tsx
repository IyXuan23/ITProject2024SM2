// Define this when using the App router API
'use client';

import { useRouter } from 'next/navigation';
import styles from '/app/style.module.css';
import HelpButton from './helpbutton';

export default function Home() {
  const router = useRouter();

  const handleSearchClick = () => {
    router.push('./search');
  };

  return (
    <>
      <main className={styles.main}>
        <img src="/image/unimelb.png" alt="Your Image" className={styles.topLeftImage} />
        <video className={styles.backgroundVideo} autoPlay loop muted>
          <source src="/video/background.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div
          id="handbook-button"
          style={{
            position: 'fixed',
            bottom: '350px',
            left: '200px',
            backgroundColor: 'transparent',
            fontFamily: 'Georgia, serif',
            color: '#ffffff',
            border: 'none',
            fontSize: '66px',
            fontWeight: '1000',
            zIndex: 1000,
          }}
        >
          HANDBOOK
        </div>
        <button
          id="search-button"
          onClick={handleSearchClick}
          style={{
            position: 'fixed',
            bottom: '250px',
            left: '200px',
            padding: '10px 20px',
            borderRadius: '50px',
            backgroundColor: 'transparent',
            fontFamily: 'Georgia, serif',
            color: '#ffffff',
            border: '3px solid #ffffff',
            fontSize: '30px',
            cursor: 'pointer',
            zIndex: 1000,
          }}
        >
          SEARCH
        </button>
        <HelpButton/>
      </main>
    </>
  );
}
