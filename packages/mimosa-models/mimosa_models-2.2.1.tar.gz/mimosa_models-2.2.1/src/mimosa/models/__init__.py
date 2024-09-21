from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from ._auto_db_schema import *  # noqa F403
from ._auto_db_schema import *  # noqa F403
from ._auto_db_schema import (
    AutoProcProgram,
    Container,
    DataCollection,
    DataCollectionGroup,
    DiffractionPlan,
    ProcessingJob,
    UserGroup,
    BLSubSample,
    BLSession,
    Protein,
    Proposal,
    Workflow,
)

__version__ = "2.2.1"

DataCollection.GridInfo = relationship("GridInfo", back_populates="DataCollection")
DataCollectionGroup.Workflow = relationship(
    "Workflow", back_populates="DataCollectionGroup"
)
Workflow.DataCollectionGroup = relationship(
    "DataCollectionGroup", back_populates="Workflow"
)

DiffractionPlan.DataCollection = relationship(
    "DataCollection", back_populates="DiffractionPlan"
)

AutoProcProgram.AutoProcProgramAttachments = relationship(
    "AutoProcProgramAttachment", back_populates="AutoProcProgram"
)
ProcessingJob.ProcessingJobParameters = relationship(
    "ProcessingJobParameter", back_populates="ProcessingJob"
)
ProcessingJob.ProcessingJobImageSweeps = relationship(
    "ProcessingJobImageSweep", back_populates="ProcessingJob"
)
ProcessingJob.AutoProcProgram = relationship(
    "AutoProcProgram", back_populates="ProcessingJob"
)

UserGroup.Permission = relationship(
    "Permission", secondary="UserGroup_has_Permission", back_populates="UserGroup"
)
UserGroup.Person = relationship(
    "Person", secondary="UserGroup_has_Person", back_populates="UserGroup"
)

Protein.ConcentrationType = relationship(
    "ConcentrationType",
    # back_populates="Protein",
    foreign_keys=[Protein.concentrationTypeId],
    primaryjoin="Protein.concentrationTypeId == ConcentrationType.concentrationTypeId",
)

BLSubSample.Position1 = relationship("Position", foreign_keys=[BLSubSample.positionId])

BLSubSample.Position2 = relationship(
    "Position", foreign_keys=[BLSubSample.position2Id], overlaps="Position"
)

Container.Dewar = relationship(
    "Dewar", primaryjoin="Container.dewarId == Dewar.dewarId"
)
Container.Dewar1 = relationship(
    "Dewar", primaryjoin="Container.currentDewarId == Dewar.dewarId"
)


class ModifiedProposal(Proposal):
    BLSession = relationship("BLSession", back_populates="Proposal")
    ProposalHasPerson = relationship("ProposalHasPerson", back_populates="Proposal")

    @hybrid_property
    def proposal(self):
        return self.proposalCode + self.proposalNumber


Proposal = ModifiedProposal


class ModifiedBLSession(BLSession):
    SessionHasPerson = relationship("SessionHasPerson", back_populates="BLSession")

    SessionType = relationship("SessionType", back_populates="BLSession")

    @hybrid_property
    def session(self):
        if self.Proposal:
            return (
                self.Proposal.proposalCode
                + self.Proposal.proposalNumber
                + "-"
                + str(self.visit_number)
            )
        else:
            return None

    @session.expression
    def session(cls):
        return func.concat(
            Proposal.proposalCode, Proposal.proposalNumber, "-", cls.visit_number
        )

    @hybrid_property
    def proposal(self):
        if self.Proposal:
            return self.Proposal.proposalCode + self.Proposal.proposalNumber
        else:
            return None

    @proposal.expression
    def proposal(cls):
        return func.concat(Proposal.proposalCode, Proposal.proposalNumber)


BLSession = ModifiedBLSession
