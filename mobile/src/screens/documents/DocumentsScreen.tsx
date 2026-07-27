import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList, Alert, ScrollView } from 'react-native';
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
  requestPublishDocument,
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
  const [isPublishing, setIsPublishing] = useState(false);

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
        type: file.mimeType || 'application/pdf',
        fileObj: (file as any).file,
      })).unwrap();

      Alert.alert('Success', 'Document uploaded successfully. AI extraction in progress.');
      dispatch(fetchDocuments());
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
          onPress: () => dispatch(deleteDocument(doc.id))
        },
      ]
    );
  };

  const handleViewSummary = async (doc: Document) => {
    setSelectedDoc(doc);
    setSummaryDialogVisible(true);
    if (!doc.ai_summary) {
      const res = await dispatch(fetchAISummary(doc.id)).unwrap();
      setSelectedDoc(prev => prev ? { ...prev, ai_summary: res.summary } : prev);
    }
  };

  const handlePublishRequest = async (doc: Document) => {
    try {
      setIsPublishing(true);
      await dispatch(requestPublishDocument(doc.id)).unwrap();
      setIsPublishing(false);
      Alert.alert(
        'Publish Request Submitted',
        'Your scheme document has been submitted to Super Admins & Content Admins for review and public publishing.'
      );
      setSummaryDialogVisible(false);
      dispatch(fetchDocuments());
    } catch (err) {
      setIsPublishing(false);
      Alert.alert('Error', 'Failed to submit publish request to admins.');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return colors.success;
      case 'processing': return colors.primary;
      case 'failed': return colors.error;
      default: return colors.warning;
    }
  };

  const renderDocumentCard = ({ item: doc }: { item: Document }) => (
    <Card style={styles.card}>
      <Card.Content style={styles.cardContent}>
        <View style={styles.cardHeader}>
          <View style={styles.docInfo}>
            <Text variant="titleMedium" style={[styles.docName, { color: colors.textPrimary }]} numberOfLines={1}>
              {doc.filename}
            </Text>
            <Text variant="bodySmall" style={styles.docSize}>
              {(doc.file_size / 1024).toFixed(1)} KB
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

          {doc.publish_status === 'pending_review' && (
            <Chip compact icon="clock-outline" style={styles.pendingChip} textStyle={{ color: '#856404' }}>
              Admin Review Pending
            </Chip>
          )}

          {doc.publish_status === 'published' && (
            <Chip compact icon="check-circle" style={styles.publishedChip} textStyle={{ color: '#155724' }}>
              Published Publicly
            </Chip>
          )}
        </View>

        <Text variant="bodySmall" style={styles.uploadedAt}>
          Uploaded: {doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleDateString('en-IN') : 'Recently'}
        </Text>

        <View style={styles.actionRow}>
          <Button 
            mode={doc.summary_generated ? "contained" : "outlined"}
            onPress={() => handleViewSummary(doc)}
            disabled={doc.status === 'processing'}
            textColor={doc.summary_generated ? '#FFFFFF' : colors.primary}
            buttonColor={doc.summary_generated ? colors.primary : undefined}
            style={styles.viewSummaryButton}
            labelStyle={{ fontSize: 13, fontWeight: '600' }}
          >
            {doc.summary_generated ? 'View AI Summary & Eligibility' : 'Processing...'}
          </Button>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text variant="headlineSmall" style={[styles.title, { color: colors.textPrimary }]}>My Documents</Text>
        <Text variant="bodyMedium" style={styles.subtitle}>
          Upload policy documents for AI extraction, eligibility criteria & admin publishing
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
              <Text variant="bodyLarge" style={{ color: colors.textPrimary, fontWeight: '600' }}>No documents yet</Text>
              <Text variant="bodyMedium" style={styles.emptySubtext}>
                Upload your dental insurance or scheme PDF documents
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
        color="#FFFFFF"
      />

      <Portal>
        <Dialog 
          visible={summaryDialogVisible} 
          onDismiss={() => setSummaryDialogVisible(false)}
          style={{ backgroundColor: colors.cardBg, borderRadius: 16 }}
        >
          <Dialog.Title style={{ color: colors.textPrimary, fontWeight: 'bold' }}>
            AI Summary & Eligibility Criteria
          </Dialog.Title>
          <Dialog.ScrollArea style={{ maxHeight: 380, paddingHorizontal: 16 }}>
            <ScrollView>
              {selectedDoc?.ai_summary ? (
                <View style={{ gap: 14, paddingVertical: 8 }}>
                  {selectedDoc.ai_summary.coverage_summary && (
                    <View style={styles.summarySection}>
                      <Text variant="titleSmall" style={[styles.sectionTitle, { color: colors.primary }]}>
                        Coverage Summary
                      </Text>
                      <Text variant="bodyMedium" style={{ color: colors.textPrimary }}>
                        {selectedDoc.ai_summary.coverage_summary}
                      </Text>
                    </View>
                  )}

                  {selectedDoc.ai_summary.eligibility_criteria && (
                    <View style={styles.summarySection}>
                      <Text variant="titleSmall" style={[styles.sectionTitle, { color: colors.primary }]}>
                        Eligibility Criteria
                      </Text>
                      <Text variant="bodyMedium" style={{ color: colors.textPrimary, lineHeight: 20 }}>
                        {selectedDoc.ai_summary.eligibility_criteria}
                      </Text>
                    </View>
                  )}
                  
                  {selectedDoc.ai_summary.exclusions && (
                    <View style={styles.summarySection}>
                      <Text variant="titleSmall" style={[styles.sectionTitle, { color: colors.primary }]}>
                        Exclusions
                      </Text>
                      <Text variant="bodyMedium" style={{ color: colors.textPrimary }}>
                        {selectedDoc.ai_summary.exclusions}
                      </Text>
                    </View>
                  )}
                  
                  {selectedDoc.ai_summary.claims_process && (
                    <View style={styles.summarySection}>
                      <Text variant="titleSmall" style={[styles.sectionTitle, { color: colors.primary }]}>
                        Claims Process
                      </Text>
                      <Text variant="bodyMedium" style={{ color: colors.textPrimary }}>
                        {selectedDoc.ai_summary.claims_process}
                      </Text>
                    </View>
                  )}

                  <View style={styles.publishBox}>
                    <Text variant="titleSmall" style={{ fontWeight: 'bold', color: colors.textPrimary }}>
                      Publish Scheme to Public
                    </Text>
                    <Text variant="bodySmall" style={{ color: colors.textSecondary, marginBottom: 8 }}>
                      Submit this document and AI scheme details to Super Admins & Content Admins for review.
                    </Text>

                    {selectedDoc.publish_status === 'pending_review' ? (
                      <Chip icon="clock-outline" style={{ backgroundColor: '#FFF3CD' }} textStyle={{ color: '#856404' }}>
                        Submitted to Admins for Review
                      </Chip>
                    ) : selectedDoc.publish_status === 'published' ? (
                      <Chip icon="check-circle" style={{ backgroundColor: '#D4EDDA' }} textStyle={{ color: '#155724' }}>
                        Published Publicly
                      </Chip>
                    ) : (
                      <Button 
                        mode="contained" 
                        buttonColor={colors.primary}
                        loading={isPublishing}
                        disabled={isPublishing}
                        onPress={() => handlePublishRequest(selectedDoc)}
                        labelStyle={{ color: '#FFFFFF', fontWeight: 'bold' }}
                      >
                        Publish Scheme to All Users
                      </Button>
                    )}
                  </View>
                </View>
              ) : (
                <ActivityIndicator style={{ marginVertical: 32 }} size="large" />
              )}
            </ScrollView>
          </Dialog.ScrollArea>
          <Dialog.Actions>
            <Button onPress={() => setSummaryDialogVisible(false)} textColor={colors.textPrimary}>
              Close
            </Button>
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
    paddingHorizontal: 12,
    paddingVertical: 14,
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
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.border,
    elevation: 2,
    overflow: 'hidden',
  },
  cardContent: {
    padding: 14,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  docInfo: {
    flex: 1,
    marginRight: 8,
  },
  docName: {
    fontWeight: 'bold',
  },
  docSize: {
    color: colors.textSecondary,
    marginTop: 2,
  },
  statusContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginTop: 8,
  },
  statusChip: {
    height: 26,
  },
  aiChip: {
    height: 26,
    backgroundColor: `${colors.primary}15`,
  },
  pendingChip: {
    height: 26,
    backgroundColor: '#FFF3CD',
  },
  publishedChip: {
    height: 26,
    backgroundColor: '#D4EDDA',
  },
  uploadedAt: {
    color: colors.textSecondary,
    marginTop: 8,
    fontSize: 12,
  },
  actionRow: {
    marginTop: 12,
    width: '100%',
  },
  viewSummaryButton: {
    borderRadius: 10,
    width: '100%',
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
    marginBottom: 8,
  },
  sectionTitle: {
    fontWeight: 'bold',
    marginBottom: 4,
  },
  publishBox: {
    marginTop: 14,
    padding: 14,
    borderRadius: 12,
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.border,
  },
  confidenceChip: {
    alignSelf: 'flex-start',
    marginTop: 8,
  },
});
