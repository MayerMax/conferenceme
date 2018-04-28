import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewSpeakerComponent } from './new-speaker.component';

describe('NewSpeakerComponent', () => {
  let component: NewSpeakerComponent;
  let fixture: ComponentFixture<NewSpeakerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewSpeakerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewSpeakerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
