import React, { useMemo } from 'react';
import { View, Text, Image, FlatList, Pressable, StyleSheet } from 'react-native';
import { GROUPS, wordsForGroup } from '../game/assignment';
import { getBookmarkImage } from '../data/images';
import { theme } from '../theme';

export default function WordsScreen({ assignment, groupKey, sessionCode, onNewGame, onBack }) {
  const group = GROUPS[groupKey];
  const rows = useMemo(() => wordsForGroup(assignment, groupKey), [assignment, groupKey]);

  return (
    <View style={styles.container}>
      <View style={styles.topRow}>
        <Pressable onPress={onBack} hitSlop={12}>
          <Text style={styles.back}>‹ Groups</Text>
        </Pressable>
        <Text style={styles.code}>Code {sessionCode}</Text>
      </View>

      <View style={[styles.groupHeader, { backgroundColor: group.color }]}>
        <Text style={styles.groupName}>{group.name}</Text>
        <Text style={styles.groupSub}>Your 8 words</Text>
      </View>

      <FlatList
        data={rows}
        keyExtractor={(item) => String(item.id)}
        contentContainerStyle={styles.list}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <Image source={getBookmarkImage(item.image)} style={styles.thumb} resizeMode="contain" />
            <View style={styles.rowText}>
              <Text style={styles.word}>{item.word}</Text>
              <Text style={styles.meta}>
                Bookmark {item.id} · {item.block}
              </Text>
            </View>
          </View>
        )}
      />

      <Pressable
        style={({ pressed }) => [styles.newGameButton, pressed && styles.pressed]}
        onPress={onNewGame}
      >
        <Text style={styles.newGameText}>Start New Game</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.bg, paddingHorizontal: 20, paddingTop: 8 },
  topRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  back: { color: theme.muted, fontSize: 17 },
  code: { color: theme.accent, fontSize: 16, fontWeight: '700', letterSpacing: 2 },
  groupHeader: { borderRadius: 16, paddingVertical: 18, paddingHorizontal: 20, marginBottom: 16 },
  groupName: { color: '#fff', fontSize: 26, fontWeight: '800' },
  groupSub: { color: 'rgba(255,255,255,0.85)', fontSize: 14, marginTop: 2 },
  list: { paddingBottom: 24, gap: 12 },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.card,
    borderRadius: 14,
    padding: 12,
    borderWidth: 1,
    borderColor: theme.border,
  },
  thumb: { width: 104, height: 104, marginRight: 18 },
  rowText: { flex: 1 },
  word: { color: theme.text, fontSize: 22, fontWeight: '700', textTransform: 'capitalize' },
  meta: { color: theme.muted, fontSize: 13, marginTop: 2, textTransform: 'capitalize' },
  newGameButton: {
    backgroundColor: theme.accent,
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 20,
  },
  newGameText: { color: '#1c1a2e', fontSize: 17, fontWeight: '800' },
  pressed: { opacity: 0.85, transform: [{ scale: 0.99 }] },
});
