import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  KeyboardAvoidingView,
  ScrollView,
  Keyboard,
  Platform,
} from 'react-native';
import { generateSessionCode } from '../game/rng';
import { theme } from '../theme';

export default function HomeScreen({ sessionCode, onStartSession }) {
  const [joinCode, setJoinCode] = useState('');
  const [error, setError] = useState('');

  function handleNewGame() {
    setError('');
    Keyboard.dismiss();
    const code = generateSessionCode();
    onStartSession(code);
  }

  function handleJoin() {
    const trimmed = joinCode.trim();
    if (!/^\d{4}$/.test(trimmed)) {
      setError('Enter a 4-digit code (0000–9999).');
      return;
    }
    setError('');
    Keyboard.dismiss();
    onStartSession(trimmed);
  }

  const canJoin = /^\d{4}$/.test(joinCode);

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.container}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.title}>Glyph-it</Text>
          <Text style={styles.subtitle}>The bookmark word game</Text>
        </View>

        {sessionCode ? (
          <View style={styles.codeBox}>
            <Text style={styles.codeLabel}>Current session code</Text>
            <Text style={styles.codeValue}>{sessionCode}</Text>
            <Text style={styles.codeHint}>Share this code with everyone at the table.</Text>
          </View>
        ) : null}

        <Pressable
          style={({ pressed }) => [styles.primaryButton, pressed && styles.pressed]}
          onPress={handleNewGame}
        >
          <Text style={styles.primaryButtonText}>New Game</Text>
          <Text style={styles.primaryButtonSub}>Organizer · generates a code</Text>
        </Pressable>

        <View style={styles.divider}>
          <View style={styles.dividerLine} />
          <Text style={styles.dividerText}>or join</Text>
          <View style={styles.dividerLine} />
        </View>

        <Text style={styles.joinLabel}>Enter the 4-digit code</Text>
        <TextInput
          style={styles.input}
          value={joinCode}
          onChangeText={(t) => setJoinCode(t.replace(/[^\d]/g, '').slice(0, 4))}
          placeholder="0000"
          placeholderTextColor={theme.muted}
          keyboardType="number-pad"
          inputMode="numeric"
          maxLength={4}
          returnKeyType="go"
          onSubmitEditing={handleJoin}
        />
        <Pressable
          style={({ pressed }) => [
            styles.joinButton,
            !canJoin && styles.joinButtonDisabled,
            pressed && styles.pressed,
          ]}
          onPress={handleJoin}
        >
          <Text style={styles.joinButtonText}>Join Game</Text>
        </Pressable>

        {error ? <Text style={styles.error}>{error}</Text> : null}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: theme.bg },
  container: {
    flexGrow: 1,
    backgroundColor: theme.bg,
    paddingHorizontal: 28,
    paddingVertical: 32,
    justifyContent: 'center',
  },
  header: { alignItems: 'center', marginBottom: 36 },
  title: { fontSize: 44, fontWeight: '800', color: theme.text, letterSpacing: 1 },
  subtitle: { fontSize: 16, color: theme.muted, marginTop: 6 },
  codeBox: {
    backgroundColor: theme.card,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 28,
    borderWidth: 1,
    borderColor: theme.border,
  },
  codeLabel: { color: theme.muted, fontSize: 13, textTransform: 'uppercase', letterSpacing: 1 },
  codeValue: {
    color: theme.accent,
    fontSize: 52,
    fontWeight: '800',
    letterSpacing: 8,
    marginVertical: 6,
  },
  codeHint: { color: theme.muted, fontSize: 13, textAlign: 'center' },
  primaryButton: {
    backgroundColor: theme.accent,
    borderRadius: 16,
    paddingVertical: 18,
    alignItems: 'center',
  },
  primaryButtonText: { color: '#1c1a2e', fontSize: 20, fontWeight: '800' },
  primaryButtonSub: { color: '#3d3410', fontSize: 13, marginTop: 2 },
  pressed: { opacity: 0.8, transform: [{ scale: 0.99 }] },
  divider: { flexDirection: 'row', alignItems: 'center', marginVertical: 24 },
  dividerLine: { flex: 1, height: 1, backgroundColor: theme.border },
  dividerText: { color: theme.muted, marginHorizontal: 12, fontSize: 13 },
  joinLabel: { color: theme.muted, fontSize: 14, marginBottom: 8, textAlign: 'center' },
  input: {
    backgroundColor: theme.surface,
    borderRadius: 14,
    paddingVertical: 14,
    paddingHorizontal: 18,
    fontSize: 30,
    color: theme.text,
    letterSpacing: 10,
    textAlign: 'center',
    borderWidth: 1,
    borderColor: theme.border,
  },
  joinButton: {
    backgroundColor: theme.surface,
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 12,
    borderWidth: 1,
    borderColor: theme.border,
  },
  joinButtonDisabled: { opacity: 0.5 },
  joinButtonText: { color: theme.text, fontSize: 18, fontWeight: '700' },
  error: { color: '#ff8787', marginTop: 12, textAlign: 'center' },
});
