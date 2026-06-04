import React, { useState, useMemo } from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import HomeScreen from './src/screens/HomeScreen';
import GroupScreen from './src/screens/GroupScreen';
import WordsScreen from './src/screens/WordsScreen';
import { buildAssignment } from './src/game/assignment';
import { generateSessionCode } from './src/game/rng';
import { theme } from './src/theme';

export default function App() {
  const [screen, setScreen] = useState('home'); // 'home' | 'group' | 'words'
  const [sessionCode, setSessionCode] = useState(null);
  const [groupKey, setGroupKey] = useState(null);

  // The full 12-bookmark assignment is derived purely from the session code,
  // so it is reproduced identically on any device using the same code.
  const assignment = useMemo(
    () => (sessionCode ? buildAssignment(sessionCode) : []),
    [sessionCode]
  );

  function startSession(code) {
    setSessionCode(code);
    setScreen('group');
  }

  function reshuffle() {
    setSessionCode(generateSessionCode());
  }

  function selectGroup(key) {
    setGroupKey(key);
    setScreen('words');
  }

  function startNewGame() {
    setGroupKey(null);
    setSessionCode(null);
    setScreen('home');
  }

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="light" />
      {screen === 'home' && (
        <HomeScreen sessionCode={sessionCode} onStartSession={startSession} />
      )}
      {screen === 'group' && (
        <GroupScreen
          sessionCode={sessionCode}
          onSelectGroup={selectGroup}
          onReshuffle={reshuffle}
          onBack={() => setScreen('home')}
        />
      )}
      {screen === 'words' && (
        <WordsScreen
          assignment={assignment}
          groupKey={groupKey}
          sessionCode={sessionCode}
          onNewGame={startNewGame}
          onBack={() => setScreen('group')}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: theme.bg },
});
