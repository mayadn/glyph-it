import React from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';
import { GROUPS } from '../game/assignment';
import { theme } from '../theme';

const ORDER = ['orange', 'green', 'purple'];

export default function GroupScreen({ sessionCode, onSelectGroup, onReshuffle, onBack }) {
  return (
    <View style={styles.container}>
      <View style={styles.topRow}>
        <Pressable onPress={onBack} hitSlop={12}>
          <Text style={styles.back}>‹ Home</Text>
        </Pressable>
        <Text style={styles.code}>Code {sessionCode}</Text>
      </View>

      <Text style={styles.title}>Choose your group</Text>

      <View style={styles.buttons}>
        {ORDER.map((key) => {
          const group = GROUPS[key];
          return (
            <Pressable
              key={key}
              style={({ pressed }) => [
                styles.groupButton,
                { backgroundColor: group.color },
                pressed && styles.pressed,
              ]}
              onPress={() => onSelectGroup(key)}
            >
              <Text style={styles.groupName}>{group.name}</Text>
              <Text style={styles.groupBlocks}>
                {group.blocks[0]} + {group.blocks[1]}
              </Text>
            </Pressable>
          );
        })}
      </View>

      <Pressable
        style={({ pressed }) => [styles.reshuffle, pressed && styles.pressed]}
        onPress={onReshuffle}
      >
        <Text style={styles.reshuffleText}>Reshuffle words (new code)</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.bg, paddingHorizontal: 24, paddingTop: 8 },
  topRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 },
  back: { color: theme.muted, fontSize: 17 },
  code: { color: theme.accent, fontSize: 16, fontWeight: '700', letterSpacing: 2 },
  title: { color: theme.text, fontSize: 30, fontWeight: '800', marginBottom: 28 },
  buttons: { gap: 16 },
  groupButton: { borderRadius: 18, paddingVertical: 26, paddingHorizontal: 22 },
  groupName: { color: '#fff', fontSize: 26, fontWeight: '800' },
  groupBlocks: { color: 'rgba(255,255,255,0.85)', fontSize: 14, marginTop: 4, textTransform: 'capitalize' },
  pressed: { opacity: 0.85, transform: [{ scale: 0.99 }] },
  reshuffle: { marginTop: 'auto', marginBottom: 24, alignItems: 'center', paddingVertical: 14 },
  reshuffleText: { color: theme.muted, fontSize: 15 },
});
