import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList, Alert } from 'react-native';
import { 
  Text, 
  Card, 
  Button, 
  FAB, 
  ActivityIndicator, 
  Chip,
  IconButton,
  Portal,
  Dialog,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useDispatch, useSelector } from 'react-redux';
import * as DocumentPicker from 'expo-document-picker';
import { RootState, AppDispatch } from '../../redux/store';
import { 
  fetchDocuments, 
  uploadDocument, 
  deleteDocument,
  fetchAISummary,
  Document,
} from '../../redux/slices/documentsSlice';
import { useTheme } from '../../contexts/ThemeContext';

export const DocumentsScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { colors } = useTheme();
  const styles = createStyles(colors);
  const { documents, isLoading, isUploading } = useSelector((state: RootState) => state.documents);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [summaryDialogVisible, setSummaryDialogVisible] = useState(false);

  useEffect(() => {
    dispatch(fetchDocuments());
  }, []);

  const handleUpload = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'image/*'],
        copyToCacheDirectory: true,
      });

      if (result.canceled) return;

      const file = result.assets[0];
      
      await dispatch(uploadDocument({
        uri: file.uri,
        name: file.name,
        type: file.mimeType || 'application/octet-stream',
      })).unwrap();

      Alert.alert('Success', 'Document uploaded successfully');
    } catch (error) {
      Alert.alert('Error', 'Failed to upload document');
    }
  };

  const handleDelete = (doc: Document) => {
    Alert.alert(
      'Delete Document',
      `Are you sure you want to delete "${doc.filename}"?`,
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: async () => {
            await dispatch(deleteDocument(doc.id));
          }
        },
      ]
    );
  };

  const handleViewSummary = async (doc: Document) => {
    if (!doc.summary_generated) {
      Alert.alert('Processing', 'AI summary is being generated. Please check back later.');
      return;
    }

    setSelectedDoc(doc);
    
    if (!doc.ai_summary) {
      await dispatch(fetchAISummary(doc.id));
    }
    
    setSummaryDialogVisible(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return colors.primary;
      case 'processing': return colors.warning;
      case 'pending': return colors.textSecondary;
      case 'failed': return colors.error;
      default: return colors.textSecondary;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const renderDocumentCard = ({ item: doc }: { item: Document }) => (
    <Card style={styles.card}>
      <Card.Content>
        <View style={styles.cardHeader}>
          <View style={styles.fileInfo}>
            <Text variant="titleMedium" numberOfLines={1}>
              {doc.filename}
            </Text>
            <Text variant="bodySmall" style={styles.fileMeta}>
              {formatFileSize(doc.file_size)} • {doc.mime_type?.split('/')[1]?.toUpperCase() || 'FILE'}
            </Text>
          </View>
          <IconButton
            icon="delete"
            size={20}
            iconColor={colors.error}
            onPress={() => handleDelete(doc)}
          />
        </View>

        <View style={styles.statusContainer}>
          <Chip 
            compact 
            style={[styles.statusChip, { backgroundColor: getStatusColor(doc.status) + '20' }]}
            textStyle={{ color: getStatusColor(doc.status) }}
          >
            {doc.status.charAt(0).toUpperCase() + doc.status.slice(1)}
          </Chip>
          
          {doc.summary_generated && (
            <Chip compact style={styles.aiChip} icon="brain" textStyle={{ color: colors.primary }}>
              AI Summary Ready
            </Chip>
          )}
        </View>

        <Text variant="bodySmall" style={styles.uploadedAt}>
          Uploaded: {new Date(doc.uploaded_at).toLocaleDateString('en-IN')}
        </Text>
      </Card.Content>
      
      <Card.Actions>
        <Button 
          mode={doc.summary_generated ? "contained" : "outlined"}
          onPress={() => handleViewSummary(doc)}
          disabled={doc.status !== 'completed'}
          textColor={doc.summary_generated ? colors.cardBg : colors.primary}
          buttonColor={doc.summary_generated ? colors.primary : undefined}
        >
          {doc.summary_generated ? 'View AI Summary' : 'Processing...'}
        </Button>
      </Card.Actions>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text variant="headlineSmall" style={[styles.title, { color: colors.textPrimary }]}>My Documents</Text>
        <Text variant="bodyMedium" style={styles.subtitle}>
          Upload policy documents for AI-powered analysis
        </Text>
      </View>

      {isLoading ? (
        <ActivityIndicator style={styles.loader} size="large" />
      ) : (
        <FlatList
          data={documents}
          renderItem={renderDocumentCard}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text variant="bodyLarge">No documents yet</Text>
              <Text variant="bodyMedium" style={styles.emptySubtext}>
                Upload your dental insurance or policy documents
              </Text>
            </View>
          }
        />
      )}

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={handleUpload}
        loading={isUploading}
        disabled={isUploading}
      />

      <Portal>
        <Dialog visible={summaryDialogVisible} onDismiss={() => setSummaryDialogVisible(false)}>
          <Dialog.Title>AI Summary</Dialog.Title>
          <Dialog.Content>
            {selectedDoc?.ai_summary ? (
              <View>
                {selectedDoc.ai_summary.coverage_summary && (
                  <View style={styles.summarySection}>
                    <Text variant="titleSmall" style={styles.sectionTitle}>Coverage</Text>
                    <Text variant="bodyMedium">{selectedDoc.ai_summary.coverage_summary}</Text>
                  </View>
                )}
                
                {selectedDoc.ai_summary.exclusions && (
                  <View style={styles.summarySection}>
                    <Text variant="titleSmall" style={styles.sectionTitle}>Exclusions</Text>
                    <Text variant="bodyMedium">{selectedDoc.ai_summary.exclusions}</Text>
                  </View>
                )}
                
                {selectedDoc.ai_summary.waiting_period && (
                  <View style={styles.summarySection}>
                    <Text variant="titleSmall" style={styles.sectionTitle}>Waiting Period</Text>
                    <Text variant="bodyMedium">{selectedDoc.ai_summary.waiting_period}</Text>
                  </View>
                )}
                
                {selectedDoc.ai_summary.claims_process && (
                  <View style={styles.summarySection}>
                    <Text variant="titleSmall" style={styles.sectionTitle}>Claims Process</Text>
                    <Text variant="bodyMedium">{selectedDoc.ai_summary.claims_process}</Text>
                  </View>
                )}

                {selectedDoc.ai_summary.confidence_score && (
                  <Chip style={styles.confidenceChip}>
                    Confidence: {selectedDoc.ai_summary.confidence_score}%
                  </Chip>
                )}
              </View>
            ) : (
              <ActivityIndicator />
            )}
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setSummaryDialogVisible(false)}>Close</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </SafeAreaView>
  );
};

const createStyles = (colors: any) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: 16,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  title: {
    fontWeight: 'bold',
  },
  subtitle: {
    color: colors.textSecondary,
    marginTop: 4,
  },
  listContent: {
    padding: 16,
  },
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: colors.primary,
  },
  card: {
    marginBottom: 12,
    backgroundColor: colors.cardBg,
    borderWidth: 1,
    borderColor: colors.border,
    elevation: 1,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  fileInfo: {
    flex: 1,
    marginRight: 8,
  },
  fileMeta: {
    color: colors.textSecondary,
    marginTop: 2,
  },
  statusContainer: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 8,
  },
  statusChip: {
    height: 24,
  },
  aiChip: {
    height: 24,
    backgroundColor: `${colors.secondary}30`,
  },
  uploadedAt: {
    color: colors.textSecondary,
    marginTop: 8,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 48,
  },
  emptySubtext: {
    color: colors.textSecondary,
    marginTop: 8,
    textAlign: 'center',
  },
  summarySection: {
    marginBottom: 12,
  },
  sectionTitle: {
    color: colors.primary,
    marginBottom: 4,
  },
  confidenceChip: {
    alignSelf: 'flex-start',
    marginTop: 8,
  },
});
